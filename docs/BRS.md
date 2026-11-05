# Business Requirements Specification (BRS)

**Product:** HydroGuard (articles-hydroguard-fdd)
*Reconstructed from the README, the requirements document, the TRL assessment and the tests of this repository. Not reviewed by the owner. A patent attorney must review before publication of method details.*

## 1. Business problem
Condition monitoring of hydraulic equipment (pumps, valves, coolers, accumulators) usually returns a single guess for each component. An operator needs to know how far to trust it, and when a cycle looks like nothing seen before.

## 2. Business objectives
| ID | Objective |
|----|-----------|
| BO-1 | Return a set of possible condition grades with a stated confidence (95%) for each component |
| BO-2 | Treat an empty set as an alarm that the cycle is out of the calibrated range |
| BO-3 | Measure what happens to coverage when operating conditions change |

## 3. Users and stakeholders (proposed; to be confirmed by the owner)
Maintenance and reliability engineers of offshore and process plants.

## 4. Scope
In scope: split-conformal diagnosis on the public UCI hydraulic-systems data (2205 cycles, 17 sensors, 4 components).
Out of scope: deployment on a plant, other rigs, automatic maintenance decisions.

## 5. Constraints and assumptions
- All data are synthetic or public benchmark data; the product makes no clinical, operational or regulatory claim.
- Maturity is TRL 4 (see docs/TRL.md).
- One test rig; cycles are split at random, so the 0.95 coverage holds for that rig only.

## 6. Success measures (to be measured on real data)
Coverage and empty-set rate on a second rig and on unstable cycles; false alarms per month in operation.
