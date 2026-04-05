"""
Achievement NFT Service

Handles minting, transferring, and marketplace operations for Achievement NFTs.
The app wallet (LEARN_WALLET_PRIVATE_KEY) pays all gas fees — users never
need CELO for gas. Marketplace balances are tracked in Supabase.
"""

import os
import json
import logging
from datetime import datetime
from web3 import Web3
from eth_account import Account

logger = logging.getLogger(__name__)

NFT_ABI = [
    {
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "quizId", "type": "string"},
            {"name": "score", "type": "uint8"},
            {"name": "total", "type": "uint8"},
            {"name": "quizName", "type": "string"},
            {"name": "_tokenURI", "type": "string"}
        ],
        "name": "mint",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "tokenId", "type": "uint256"}
        ],
        "name": "transferByOperator",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "getTokenData",
        "outputs": [
            {"name": "tokenOwner", "type": "address"},
            {"name": "quizId", "type": "string"},
            {"name": "score", "type": "uint8"},
            {"name": "total", "type": "uint8"},
            {"name": "quizName", "type": "string"},
            {"name": "mintedAt", "type": "uint256"},
            {"name": "uri", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "getOwnerTokens",
        "outputs": [{"name": "", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]


class AchievementNFTService:
    """Service for minting and transferring Achievement NFTs — app pays all gas."""

    def __init__(self):
        self.celo_rpc_url = os.getenv('CELO_RPC_URL', 'https://forno.celo.org')
        self.chain_id = int(os.getenv('CHAIN_ID', 42220))
        self.contract_address = os.getenv('ACHIEVEMENT_NFT_CONTRACT_ADDRESS')
        self._wallet_key = os.getenv('LEARN_WALLET_PRIVATE_KEY')

        self.w3 = Web3(Web3.HTTPProvider(self.celo_rpc_url, request_kwargs={'timeout': 30}))
        self.contract = None
        self.operator_account = None

        self._initialize()

    def _initialize(self):
        try:
            if not self.w3.is_connected():
                logger.error("Failed to connect to Celo network for NFT service")
                return

            if self.contract_address:
                self.contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(self.contract_address),
                    abi=NFT_ABI
                )
                logger.info(f"Achievement NFT contract loaded: {self.contract_address[:10]}...")
            else:
                logger.warning("ACHIEVEMENT_NFT_CONTRACT_ADDRESS not set — deploy contract first")

            if self._wallet_key:
                key = self._wallet_key if self._wallet_key.startswith('0x') else '0x' + self._wallet_key
                self.operator_account = Account.from_key(key)
                logger.info(f"NFT operator wallet configured: {self.operator_account.address[:10]}...")
            else:
                logger.error("LEARN_WALLET_PRIVATE_KEY not configured")

        except Exception as e:
            logger.error(f"NFT service initialization error: {e}")

    @property
    def is_configured(self) -> bool:
        return self.contract is not None and self.operator_account is not None

    def _send_transaction(self, txn_builder, gas_limit=500000) -> dict:
        try:
            nonce = self.w3.eth.get_transaction_count(self.operator_account.address)
            gas_price = int(self.w3.eth.gas_price * 1.2)

            txn = txn_builder.build_transaction({
                'chainId': self.chain_id,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': nonce,
            })

            signed = self.w3.eth.account.sign_transaction(txn, self._wallet_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
            tx_hash_hex = tx_hash.hex()

            if not tx_hash_hex.startswith('0x'):
                tx_hash_hex = '0x' + tx_hash_hex

            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            if receipt.status != 1:
                logger.error(f"❌ Transaction REVERTED on-chain: tx={tx_hash_hex} status={receipt.status} gasUsed={receipt.gasUsed}")
                return {
                    "success": False,
                    "tx_hash": tx_hash_hex,
                    "error": f"Transaction reverted on-chain (tx={tx_hash_hex[:18]}...). Check celoscan.io for details.",
                    "gas_used": receipt.gasUsed,
                }

            return {
                "success": True,
                "tx_hash": tx_hash_hex,
                "gas_used": receipt.gasUsed,
                "block_number": receipt.blockNumber,
                "explorer_url": f"https://celoscan.io/tx/{tx_hash_hex}"
            }

        except Exception as e:
            logger.error(f"NFT transaction error: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def mint_nft(self, to_address: str, quiz_id: str, score: int, total: int,
                 quiz_name: str) -> dict:
        """
        Mint an Achievement NFT to a user's wallet. App pays gas.

        Args:
            to_address: User's wallet address
            quiz_id: Quiz identifier
            score: Number of correct answers
            total: Total number of questions
            quiz_name: Name of the quiz

        Returns:
            dict with success, token_id, tx_hash
        """
        if not self.is_configured:
            return {"success": False, "error": "NFT service not configured. Deploy contract first."}

        try:
            percentage = round((score / total) * 100) if total > 0 else 0
            token_uri = self._build_token_uri(quiz_id, score, total, quiz_name, percentage, to_address)

            result = self._send_transaction(
                self.contract.functions.mint(
                    Web3.to_checksum_address(to_address),
                    quiz_id,
                    score,
                    total,
                    quiz_name,
                    token_uri
                ),
                gas_limit=1500000
            )

            if result["success"]:
                receipt = self.w3.eth.get_transaction_receipt(result["tx_hash"])
                token_id = self._extract_token_id_from_receipt(receipt)
                result["token_id"] = token_id
                logger.info(f"NFT minted: token #{token_id} -> {to_address[:10]}...")

            return result

        except Exception as e:
            logger.error(f"Mint error: {e}")
            return {"success": False, "error": str(e)}

    def transfer_nft(self, from_address: str, to_address: str, token_id: int) -> dict:
        """
        Transfer NFT using operator privileges. App pays gas.

        Args:
            from_address: Current owner's wallet address
            to_address: Buyer's wallet address
            token_id: NFT token ID

        Returns:
            dict with success, tx_hash
        """
        if not self.is_configured:
            return {"success": False, "error": "NFT service not configured"}

        try:
            current_owner = self.contract.functions.ownerOf(token_id).call()
            if current_owner.lower() != from_address.lower():
                return {"success": False, "error": "Token owner mismatch"}

            result = self._send_transaction(
                self.contract.functions.transferByOperator(
                    Web3.to_checksum_address(from_address),
                    Web3.to_checksum_address(to_address),
                    token_id
                ),
                gas_limit=300000
            )

            if result["success"]:
                logger.info(f"NFT #{token_id} transferred: {from_address[:10]}... -> {to_address[:10]}...")

            return result

        except Exception as e:
            logger.error(f"Transfer error: {e}")
            return {"success": False, "error": str(e)}

    def get_token_data(self, token_id: int) -> dict:
        """Get on-chain data for a token"""
        if not self.is_configured:
            return {}

        try:
            data = self.contract.functions.getTokenData(token_id).call()
            return {
                "token_id": token_id,
                "owner": data[0],
                "quiz_id": data[1],
                "score": data[2],
                "total": data[3],
                "quiz_name": data[4],
                "minted_at": datetime.fromtimestamp(data[5]).isoformat() if data[5] else None,
                "token_uri": data[6],
                "explorer_url": f"https://celoscan.io/token/{self.contract_address}?a={token_id}"
            }
        except Exception as e:
            logger.error(f"Error getting token data: {e}")
            return {}

    def get_owner_tokens(self, wallet_address: str) -> list:
        """Get all token IDs owned by a wallet"""
        if not self.is_configured:
            return []

        try:
            token_ids = self.contract.functions.getOwnerTokens(
                Web3.to_checksum_address(wallet_address)
            ).call()
            return [int(t) for t in token_ids]
        except Exception as e:
            logger.error(f"Error getting owner tokens: {e}")
            return []

    def get_operator_address(self) -> str:
        """Return the operator (app) wallet address"""
        if self.operator_account:
            return self.operator_account.address
        return ''

    def verify_g_transfer(self, tx_hash: str, from_address: str, to_address: str, amount_g: float, retries: int = 3) -> dict:
        """
        Verify that a G$ transfer(from → to, amount) occurred in tx_hash.
        The user sends G$ directly via transfer() — no approve/transferFrom needed.

        Args:
            tx_hash:      Transaction hash of the user's transfer() tx
            from_address: Expected sender (buyer)
            to_address:   Expected recipient (seller)
            amount_g:     Required amount in G$ (human-readable)
            retries:      Times to retry if tx not yet mined

        Returns:
            dict with success, verified
        """
        import time
        g_dollar_address = os.getenv('G_DOLLAR_TOKEN_ADDRESS', '0x62B8B11039FcfE5aB0C56E502b1C372A3d2a9c7A').lower()
        # keccak256("Transfer(address,address,uint256)")
        transfer_topic = self.w3.keccak(text="Transfer(address,address,uint256)").hex()
        if not transfer_topic.startswith('0x'):
            transfer_topic = '0x' + transfer_topic
        amount_wei = int(amount_g * (10 ** 18))

        for attempt in range(retries):
            try:
                receipt = self.w3.eth.get_transaction_receipt(tx_hash)
                if receipt is None:
                    logger.info(f"Tx {tx_hash[:18]}... not yet mined, waiting... (attempt {attempt+1}/{retries})")
                    time.sleep(5)
                    continue

                if receipt.status != 1:
                    return {"success": False, "error": f"G$ payment transaction failed on-chain (status=0). tx={tx_hash[:18]}..."}

                # Decode Transfer events from the G$ token contract
                for log in receipt.logs:
                    if log.address.lower() != g_dollar_address:
                        continue
                    if not log.topics or log.topics[0].hex() not in (transfer_topic, transfer_topic.lstrip('0x')):
                        continue
                    if len(log.topics) < 3:
                        continue

                    log_from = '0x' + log.topics[1].hex()[-40:]
                    log_to   = '0x' + log.topics[2].hex()[-40:]
                    log_amt  = int(log.data.hex(), 16) if log.data else 0

                    logger.info(f"🔍 Transfer event: from={log_from[:10]}... to={log_to[:10]}... amount={log_amt / 10**18:.4f} G$")

                    if (log_from.lower() == from_address.lower()
                            and log_to.lower() == to_address.lower()
                            and log_amt >= amount_wei):
                        logger.info(f"✅ G$ transfer verified: {amount_g} G$ buyer→seller tx={tx_hash[:18]}...")
                        return {"success": True, "verified": True, "tx_hash": tx_hash}

                return {"success": False, "error": f"G$ Transfer event not found in tx. Expected {amount_g} G$ from buyer to seller. tx={tx_hash[:18]}..."}

            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(3)
                    continue
                logger.error(f"verify_g_transfer error: {e}", exc_info=True)
                return {"success": False, "error": str(e)}

        return {"success": False, "error": "G$ payment tx not yet mined after retries. Please try again in a moment."}

    def burn_nft(self, owner_address: str, token_id: int) -> dict:
        """
        Burn an NFT by transferring it to the dead address (0x000...dEaD).
        App wallet pays gas via operator privilege.

        Args:
            owner_address: Current owner's wallet address
            token_id: NFT token ID to burn

        Returns:
            dict with success, tx_hash
        """
        if not self.is_configured:
            return {"success": False, "error": "NFT service not configured"}

        dead_address = Web3.to_checksum_address("0x000000000000000000000000000000000000dEaD")

        try:
            current_owner = self.contract.functions.ownerOf(token_id).call()
            if current_owner.lower() != owner_address.lower():
                return {"success": False, "error": "Token owner mismatch — cannot burn NFT you do not own"}

            result = self._send_transaction(
                self.contract.functions.transferByOperator(
                    Web3.to_checksum_address(owner_address),
                    dead_address,
                    token_id
                ),
                gas_limit=300000
            )

            if result["success"]:
                logger.info(f"🔥 NFT #{token_id} burned by {owner_address[:10]}... → dEaD")

            return result

        except Exception as e:
            logger.error(f"Burn error: {e}")
            return {"success": False, "error": str(e)}

    def get_total_supply(self) -> int:
        """Get total number of minted NFTs"""
        if not self.is_configured:
            return 0

        try:
            return self.contract.functions.totalSupply().call()
        except Exception as e:
            logger.error(f"Error getting total supply: {e}")
            return 0

    def _extract_token_id_from_receipt(self, receipt) -> int:
        """Extract token ID from the Transfer event in receipt"""
        try:
            transfer_topic = self.w3.keccak(text="Transfer(address,address,uint256)").hex()
            for log in receipt.logs:
                if len(log.topics) >= 4 and log.topics[0].hex() == transfer_topic:
                    if log.topics[1].hex().endswith('0' * 24):
                        token_id = int(log.topics[3].hex(), 16)
                        return token_id
            total = self.contract.functions.totalSupply().call()
            return total
        except Exception as e:
            logger.warning(f"Could not extract token ID from receipt: {e}")
            try:
                return self.contract.functions.totalSupply().call()
            except Exception:
                return 0

    def _build_token_uri(self, quiz_id: str, score: int, total: int,
                         quiz_name: str, percentage: int, owner: str) -> str:
        """Build a compact base64-encoded JSON token URI (on-chain metadata)"""
        import base64

        metadata = {
            "name": f"GMA: {quiz_name}",
            "description": f"GoodMarket Achievement NFT — {quiz_name} ({score}/{total})",
            "attributes": [
                {"trait_type": "Quiz", "value": quiz_name},
                {"trait_type": "Score", "value": f"{score}/{total}"},
                {"trait_type": "Pct", "value": f"{percentage}%"},
                {"trait_type": "Platform", "value": "GoodMarket"}
            ]
        }

        json_str = json.dumps(metadata, separators=(',', ':'))
        encoded = base64.b64encode(json_str.encode()).decode()
        return f"data:application/json;base64,{encoded}"


achievement_nft_service = AchievementNFTService()
