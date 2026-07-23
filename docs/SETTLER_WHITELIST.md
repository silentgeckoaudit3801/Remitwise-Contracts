# Settler Whitelist Operator Guide

Audience: operators and reviewers responsible for managing settlement permissions in RemitWise deployments.

This guide captures the expected operating model for adding, rotating, and revoking authorized settlers. Use it as a runbook when reviewing whitelist changes, preparing deployment checklists, or validating that off-chain settlement services are aligned with on-chain permissions.

## Scope

A settler is an operational account or service identity allowed to submit settlement-related actions for the deployment. Settler permissions should be narrower than owner, pause-admin, upgrade-admin, or emergency roles.

This guide covers:

- adding a new settler to the whitelist
- rotating from an old settler address to a new one
- revoking a compromised, retired, or temporary settler
- verifying that the effective whitelist matches the intended operator roster

This guide does not replace the contract-specific authorization matrix. When a contract exposes a dedicated settler entrypoint, treat that contract's code and tests as the source of truth for exact function names and emitted events.

## Operator Records

Track each approved settler in an operator register before making contract changes.

| Field | Required | Notes |
| --- | --- | --- |
| Settler address | yes | Stellar account or contract address used for settlement calls. |
| Owner team | yes | Team or service responsible for the key. |
| Environment | yes | `testnet`, `mainnet`, staging, or another named network. |
| Permission reason | yes | Short reason the settler needs access. |
| Activation ledger/time | yes | When the address may begin submitting settlement calls. |
| Rotation partner | if rotating | New or old address associated with the same service. |
| Revocation reason | if revoked | Compromise, retirement, temporary access expiry, or operator offboarding. |

Keep this register outside the contract repo if it contains private operational details. Public docs and PRs should only describe the control process, not secrets or private infrastructure.

## Add a Settler

1. Confirm the requested address is controlled by the intended operator.
2. Confirm the operator has a business need for settlement permissions in the target environment.
3. Check the current whitelist and verify the address is not already active.
4. Submit the contract transaction or migration that adds the address.
5. Record the transaction hash, ledger, environment, and approving operator.
6. Verify the address is active with a read-only query or by inspecting the emitted event/indexer output.
7. Announce the activation to downstream services that depend on the settler roster.

Post-change checks:

- The new settler appears exactly once in the effective whitelist.
- Existing settlers remain unchanged unless the change was a rotation.
- Non-settler addresses still fail the authorized-settler guard.
- Pause, upgrade, owner, and emergency roles are unchanged.

## Rotate a Settler

Use rotation when the same service moves from one signing address to another.

1. Add the replacement settler first when dual-running is safe.
2. Verify the replacement can perform the required settlement path in the target environment.
3. Move off-chain scheduling, monitoring, and alert routing to the replacement address.
4. Revoke the old settler after the replacement is confirmed active.
5. Record both addresses and the rotation reason in the operator register.

If dual-running is not safe, schedule a short maintenance window and perform add/revoke/verify as one controlled change.

Rotation acceptance checks:

- The old address no longer passes the settler guard after revocation.
- The new address passes the settler guard.
- There is no interval where an unapproved address is authorized.
- Monitoring dashboards and runbooks reference the new address.

## Revoke a Settler

Revoke immediately when a settler key is compromised, retired, no longer operated, or no longer has a settlement need.

1. Identify the address and environment.
2. Pause or stop the off-chain settlement service if the address may still submit transactions.
3. Submit the revocation transaction.
4. Verify the address no longer appears in the whitelist.
5. Verify calls from the revoked address fail with the expected authorization error.
6. Update the operator register with the revocation reason and transaction hash.
7. Notify downstream operators if settlement capacity changed.

Emergency revocations should prefer safety over batching. Do not wait for unrelated whitelist cleanup if a key may be compromised.

## Verification Checklist

Before marking a whitelist change complete, capture evidence for each item below.

- Target network and contract ID are correct.
- Caller had the required admin authority for the whitelist change.
- Add/rotate/revoke transaction succeeded and has a recorded transaction hash.
- Effective whitelist after the change matches the intended roster.
- Unauthorized addresses are rejected by the settler guard.
- Any emitted events or indexer rows match the address and action.
- Operator register and deployment notes are updated.
- No unrelated roles, pause channels, or upgrade settings changed.

## Review Guidance

When reviewing a PR or deployment plan that changes settler access, ask for:

- the reason each address needs settlement permissions
- the expected lifetime of temporary settlers
- proof that the old address was revoked during rotations
- the verification command, query, or event evidence used after the change
- rollback steps if the wrong address is added

Keep settlement access minimal. Prefer one address per service and environment, and avoid broad administrative keys as settlers unless the contract design explicitly requires it.