import hashlib
import hmac

from simple_ctx_log import Logger, parse_signed_logs, recompute_hash_chain


# def test_log_signing_integrity(capsys):
#     logger = Logger(signing_key=None)
#     logger.log("first message")
#     logger.log("second message")
#     logger.log("third message")
#     output = capsys.readouterr().out
#     entries = parse_signed_logs(output)

#     assert len(entries) == 3

#     messages = [msg for msg, _ in entries]
#     hashes = [sig for _, sig in entries]
#     recomputed = recompute_hash_chain(messages)

#     assert hashes == recomputed


def test_log_signing_with_hmac_key(capsys):
    key = b"super-secret-key"
    logger = Logger(signing_key=key)
    logger.log("alpha")
    logger.log("beta")
    output = capsys.readouterr().out
    entries = parse_signed_logs(output)
    messages = [msg for msg, _ in entries]
    hashes = [sig for _, sig in entries]
    recomputed = recompute_hash_chain(messages, key=key)
    assert hashes == recomputed


def test_log_signing_detects_message_tampering(capsys):
    logger = Logger()
    logger.log("original")
    logger.log("unchanged")
    output = capsys.readouterr().out
    entries = parse_signed_logs(output)
    messages = [msg for msg, _ in entries]
    hashes = [sig for _, sig in entries]

    # Tamper with first message
    messages[0] = messages[0].replace("original", "tampered")
    recomputed = recompute_hash_chain(messages)
    assert hashes != recomputed


def test_log_signing_detects_missing_log(capsys):
    logger = Logger()
    logger.log("one")
    logger.log("two")
    logger.log("three")
    output = capsys.readouterr().out
    entries = parse_signed_logs(output)
    messages = [msg for msg, _ in entries]
    hashes = [sig for _, sig in entries]

    # Remove middle log
    del messages[1]
    recomputed = recompute_hash_chain(messages)
    assert hashes[: len(recomputed)] != recomputed


def test_log_signing_detects_injected_log(capsys):
    logger = Logger()
    logger.log("first")
    logger.log("second")
    output = capsys.readouterr().out
    entries = parse_signed_logs(output)
    messages = [msg for msg, _ in entries]
    hashes = [sig for _, sig in entries]

    # Inject a fake log entry
    messages.insert(1, "FAKE LOG ENTRY")
    recomputed = recompute_hash_chain(messages)

    assert hashes != recomputed
