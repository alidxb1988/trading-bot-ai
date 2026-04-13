---
name: diaw-m05-appgenesis
description: >
  APP-GENESIS: AI-powered mobile app development module. Designs and builds
  production-ready iOS and Android applications using React Native or Flutter.
  Handles UI/UX design, backend integration, app store submission, push
  notifications, analytics, and monetization. Activates on APP-GENESIS,
  mobile app, iOS, Android, React Native, Flutter, app development.
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

# APP-GENESIS: Mobile App Development Module v3.0

## Agent Swarm Configuration
- **Topology**: Hierarchical | **Max Agents**: 5 | **Quality Gate**: 0.97
- **Agents**: App Architect, UI/UX Agent, Frontend Agent, Integration Agent, QA Agent

## Development Approach

### Tech Stack Defaults
| Layer | React Native Stack | Flutter Stack |
|-------|------------------|---------------|
| Framework | React Native 0.74+ | Flutter 3.x |
| State | Redux Toolkit / Zustand | Riverpod / BLoC |
| Navigation | React Navigation 6 | GoRouter |
| Backend | REST + WebSocket | REST + gRPC |
| Auth | Clerk / Firebase Auth | Firebase Auth |
| Analytics | Mixpanel + Firebase | Firebase + Amplitude |
| Payments | Stripe SDK | Stripe SDK |

### Development Phases
```
Phase 1: Discovery (2-3 days)
  - Feature requirements gathering
  - User persona and journey mapping
  - Wireframe and information architecture
  - Tech stack decision

Phase 2: UI/UX Design (3-5 days)
  - High-fidelity mockups (Figma)
  - Design system (colors, typography, components)
  - Prototype for user testing
  - Dark mode support

Phase 3: Core Development (1-3 weeks)
  - Screen implementation
  - Navigation and routing
  - API integration
  - Authentication flow
  - Push notifications

Phase 4: Advanced Features
  - Offline mode with local storage sync
  - Biometric authentication
  - Deep links and universal links
  - In-app purchases (StoreKit 2 / Play Billing)
  - Background sync

Phase 5: QA & Launch
  - Device testing matrix (iPhone 12-16, Android 10-14)
  - Performance profiling (render time, memory)
  - App Store / Play Store submission
  - ASO (App Store Optimization)
```

### Monetization Models
- **Freemium**: Free with premium features
- **Subscription**: Monthly/annual via in-app purchase
- **Pay-once**: One-time purchase price
- **Marketplace**: Commission on in-app transactions
- **Ad-supported**: AdMob / MoPub integration

## Revenue Model
- **Subscription**: $380/mo
- **App Build Fee**: $5,000-$25,000 per app
- **Monthly Maintenance**: $500-$2,000/mo
- **Credits**: 25-75 per app build

## Example Invocations
- "APP-GENESIS: Build a React Native trading app for ALPHA-OMEGA with real-time charts"
- "Create a Flutter delivery tracking app with push notifications and maps integration"
- "APP-GENESIS: Design and develop a loyalty rewards app for a UAE retail chain"
