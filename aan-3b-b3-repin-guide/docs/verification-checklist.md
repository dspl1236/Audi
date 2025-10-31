# Verification Checklist (Pre-Start)

## Continuity
- Grounds (T55: 10, 19, 24, 30, 51) < 0.3 Ω to chassis
- ECU power feeds present: 18 (Batt+), 27 (IGN+), 37 (injector/MAF feed)

## Sensors (Key ON)
- TPS switches (52 idle, 54 WOT) toggle low when closed; 55 ground present
- CLT (45), IAT (44) read ~3–4 V cold (NTC sensors)
- MAF (7 signal, 26 ref) present; AAN burn-off (25) removed for 3B
- Crank (49) and cam (8) produce AC pulses while cranking (shielded)

## Relays
- J271 (ECU power) energizes on IGN
- J17 (fuel pump) grounded by ECU while cranking/running

## Diagnostics & MIL
- K-line comms with 2×2 adapter
- MIL (22) on with key, off after start
