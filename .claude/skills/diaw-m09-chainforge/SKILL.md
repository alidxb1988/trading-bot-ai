---
name: diaw-m09-chainforge
description: >
  CHAIN-FORGE: AI-powered blockchain development module. Builds smart contracts,
  DeFi protocols, NFT platforms, DAOs, tokenization solutions, and Web3 dApps.
  Handles Solidity development, contract auditing, gas optimization, and
  multi-chain deployment. Activates on CHAIN-FORGE, blockchain, smart contract,
  DeFi, NFT, DAO, Web3, Solidity, tokenization, dApp.
user-invocable: true
context: fork
effort: high
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__ruflo__*
  - mcp__github__*
---

# CHAIN-FORGE: Blockchain Development Module v3.0

## Agent Swarm Configuration
- **Topology**: Red-Team/Blue-Team | **Max Agents**: 5 | **Quality Gate**: 0.99
- **Agents**: Smart Contract Developer, Security Auditor, Gas Optimizer, Frontend Agent, Deployment Agent

## Smart Contract Development Standards

### Solidity Best Practices
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Use OpenZeppelin for standard functionality
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

// Always include:
// 1. ReentrancyGuard for any ETH/token movements
// 2. Access control (Ownable or AccessControl)
// 3. Events for all state changes
// 4. Input validation at function entry
// 5. CEI pattern (Checks, Effects, Interactions)
```

### Contract Types Library
| Contract Type | Standard | Use Case |
|--------------|----------|----------|
| Fungible Token | ERC-20 | Utility tokens, governance tokens |
| NFT | ERC-721 | Collectibles, certificates, memberships |
| Semi-fungible | ERC-1155 | Gaming items, multi-edition NFTs |
| Governance | ERC-20 + Governor | DAO voting, protocol governance |
| Staking | Custom | Yield farming, liquidity mining |
| Vesting | Custom | Team/investor token vesting |
| Multisig | Safe (Gnosis) | Team treasury management |
| Proxy | UUPS / TransparentProxy | Upgradeable contracts |

### Security Audit Checklist
```
[ ] Reentrancy attacks (CEI pattern enforced)
[ ] Integer overflow/underflow (Solidity 0.8+ auto-checks)
[ ] Access control (all sensitive functions protected)
[ ] Front-running protection (commit-reveal, flash loan guards)
[ ] Oracle manipulation (TWAP oracles, multiple sources)
[ ] Flash loan attack vectors
[ ] Sandwich attack prevention for AMMs
[ ] Denial of service (gas limit, push vs pull patterns)
[ ] Centralization risks (admin keys, upgrade mechanisms)
[ ] Timestamp dependence (block.timestamp usage)
```

### Multi-Chain Deployment
| Chain | Native Token | Gas Cost | Speed |
|-------|-------------|---------|-------|
| Ethereum | ETH | High | 12s blocks |
| Polygon | MATIC | Low | 2s blocks |
| Arbitrum | ETH (L2) | Very Low | <1s |
| Base | ETH (L2) | Very Low | <1s |
| BNB Chain | BNB | Low | 3s blocks |

### Gas Optimization Techniques
```solidity
// 1. Pack storage variables (use uint128 instead of uint256 when possible)
// 2. Use calldata instead of memory for read-only arrays
// 3. Cache storage variables in local memory in loops
// 4. Use events instead of storage for historical data
// 5. Batch operations to amortize fixed costs
// 6. Use mappings over arrays when order doesn't matter
// 7. Short-circuit conditions (cheap checks first)
```

## Testing & Deployment
```bash
# Foundry test suite
forge test -vvv --gas-report
forge coverage --report lcov

# Security tools
slither . --print human-summary
mythril analyze contracts/MyContract.sol

# Deployment
forge script script/Deploy.s.sol --rpc-url $RPC_URL --broadcast --verify
```

## Revenue Model
- **Subscription**: $600/mo
- **Contract Audit**: $2,000-$10,000 per audit
- **Custom Development**: $5,000-$50,000 per project
- **Credits**: 25-75 per contract deployment

## Example Invocations
- "CHAIN-FORGE: Build a staking contract for a governance token with 30-day lock-up"
- "Audit this Solidity contract for reentrancy and access control vulnerabilities"
- "CHAIN-FORGE: Create an NFT marketplace with royalties and batch minting on Polygon"
