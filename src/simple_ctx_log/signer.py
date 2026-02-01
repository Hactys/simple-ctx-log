import hashlib
import hmac
from typing import Optional


def parse_signed_logs(output: str) -> list[tuple[str, str]]:
    """
    Parse the logger output into (exact_signed_message, hash) pairs.

    The reconstructed message must match EXACTLY what was signed
    (i.e. without the trailing newline added by print()).
    """
    entries = []
    current_lines = []

    lines = output.splitlines(keepends=True)

    for line in lines:
        if line.startswith("[hash=") and line.rstrip().endswith("]"):
            signature = line.strip()[len("[hash=") : -1]

            # Join lines and remove the LAST newline only
            message = "".join(current_lines)
            if message.endswith("\n"):
                message = message[:-1]

            entries.append((message, signature))
            current_lines = []
        else:
            current_lines.append(line)

    return entries


def recompute_hash_chain(messages: list[str], key: bytes | None = None) -> list[str]:
    last_hash = b"\x00" * hashlib.sha256().digest_size
    result = []

    for msg in messages:
        data = last_hash + msg.encode("utf-8")
        if key:
            digest = hmac.new(key, data, hashlib.sha256).digest()
        else:
            digest = hashlib.sha256(data).digest()
        last_hash = digest
        result.append(digest.hex())

    return result


class LogSigner:
    """
    Cryptographic hash chain signer for log integrity.
    """

    def __init__(self, key: Optional[bytes] = None, hash_algo: str = "sha256"):
        self._key = key or b"\x00"
        self._hash_algo = hash_algo
        self._last_hash = b"\x00" * hashlib.new(hash_algo).digest_size

    def sign(self, message: str) -> str:
        """
        Compute the next hash in the chain.

        Returns the hexadecimal digest.
        """
        data = self._last_hash + message.encode("utf-8")

        if self._key:
            digest = hmac.new(self._key, data, self._hash_algo).digest()
        else:
            h = hashlib.new(self._hash_algo)
            h.update(data)
            digest = h.digest()

        self._last_hash = digest
        return digest.hex()
