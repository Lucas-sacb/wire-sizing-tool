# Electric Wire Sizing Tool (AWG)

A Python tool for **electrical wire sizing and performance analysis** in high-power systems such as:

* Electric aircraft propulsion
* UAV power systems
* Aeromodelling / SAE Aerodesign aircraft
* High current battery systems

The tool estimates the **minimum AWG wire size** required based on electrical, thermal and mission profile constraints, and provides detailed performance analysis including:

* Electrical losses
* Wire mass
* System efficiency
* Estimated steady-state wire temperature
* Safety evaluation

---

# Features

✔ AWG sizing based on multiple engineering constraints
✔ RMS current estimation from mission profile
✔ Voltage drop analysis (FAA guideline compatible)
✔ Thermal equilibrium estimation
✔ Wire mass estimation
✔ Electrical efficiency analysis
✔ Loss vs AWG visualization

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Lucas-sacb/wire-sizing-tool.git
cd wire-sizing-tool
```

Install dependencies:

```bash
pip install matplotlib
```

---

# Usage

Run the CLI tool:

```bash
python wire_sizing.py
```

Example input:

```
Motor peak power [W]: 3000
Battery voltage [V]: 22.2
Wire length (one direction) [m]: 0.5
Takeoff time [s]: 4
Total flight time [s]: 400
```

Example output:

```
Recommended wire:

AWG: 10
Peak current: 135.14 A
RMS current: 82.70 A
Minimum area required: 4.11 mm²

AWG analysis:

AWG  4 | Loss =  14.51 W | Mass =  189.5 g | Efficiency = 99.52% | Temp =   50.4 °C | SAFE
AWG  6 | Loss =  23.07 W | Mass =  119.2 g | Efficiency = 99.24% | Temp =   76.0 °C | SAFE
AWG  8 | Loss =  36.65 W | Mass =   75.0 g | Efficiency = 98.79% | Temp =  127.1 °C | SAFE
AWG 10 | Loss =  58.33 W | Mass =   47.1 g | Efficiency = 98.09% | Temp =  230.0 °C | SAFE
AWG 12 | Loss =  92.69 W | Mass =   29.7 g | Efficiency = 97.00% | Temp =  435.6 °C | NOT SAFE
AWG 14 | Loss = 147.50 W | Mass =   18.6 g | Efficiency = 95.31% | Temp =  849.3 °C | NOT SAFE
AWG 16 | Loss = 234.19 W | Mass =   11.7 g | Efficiency = 92.76% | Temp = 1674.2 °C | NOT SAFE
AWG 18 | Loss = 374.14 W | Mass =    7.3 g | Efficiency = 88.91% | Temp = 3355.1 °C | NOT SAFE
AWG 20 | Loss = 589.99 W | Mass =    4.7 g | Efficiency = 83.57% | Temp = 6619.3 °C | NOT SAFE
```

A graph of **AWG vs power loss** is also generated automatically.

---

# Engineering Model

The sizing algorithm combines **electrical and thermal constraints**.

---

## Peak Current

$$
I_{peak} = \frac{P}{V}
$$

Where:

- $P$ = motor peak power  
- $V$ = battery voltage  

---

## RMS Current (Mission Profile)

The thermal load is computed using the RMS current over the mission:

$$
I_{RMS} =
\sqrt{
\frac{
I_{peak}^2 t_{peak} +
I_{cruise}^2 (t_{total}-t_{peak})
}{t_{total}}
}
$$

Where:

- $t_{peak}$ = takeoff duration  
- $t_{total}$ = mission time  
- $I_{cruise}$ = cruise current  

---

## Voltage Drop Constraint

Maximum voltage drop is limited by:

$$
\Delta V \leq 2\%
$$

This follows common aviation practices (e.g. FAA AC 43.13-1B).

Wire cross-section must satisfy:

$$
A \geq \frac{\rho L I}{\Delta V}
$$

---

## Thermal Constraint

Current density limit:

$$
J = \frac{I}{A}
$$

Typical silicone wire safe density:

```
J_max ≈ 20 A/mm²
```

---


---

## Electrical Losses

$$
P_{loss} = I^2 R
$$

Where:

$$
R = \frac{\rho L}{A}
$$

---

## Wire Temperature Estimation

Thermal equilibrium is estimated via convective cooling:

$$
P_{loss} = h A_{surf} (T - T_{amb})
$$

Where:

- $h$ = convection coefficient  
- $A_{surf}$ = wire surface area

---

# Output Metrics

For each AWG the tool computes:

| Metric      | Description                                   |
| ----------- | --------------------------------------------- |
| Power Loss  | Electrical heating in the wire                |
| Efficiency  | Electrical efficiency of the cable            |
| Wire Mass   | Copper mass contribution                      |
| Temperature | Estimated steady-state temperature            |
| Safety      | Whether temperature is below insulation limit |

---

# Example Use Case

Electric propulsion system:

| Parameter    | Value            |
| ------------ | ---------------- |
| Motor Power  | 3000 W           |
| Battery      | 6S LiPo (22.2 V) |
| Cable Length | 0.5 m            |
| Takeoff Time | 4 s              |
| Flight Time  | 300 s            |

Recommended cable:

```
AWG 10
```

---

# Project Structure

```
wire-sizing-tool/
│
├── wire_sizing.py
├── README.md
├── requirements.txt
└── LICENSE
```

---

# Requirements

```
Python ≥ 3.8
matplotlib
```

---

# Potential Applications

* Electric aircraft design
* UAV propulsion systems
* Battery pack wiring
* Robotics power distribution
* SAE Aerodesign projects

---

# License

MIT License

---

# Author

Lucas Santos

Aeronautical Engineering Student
UNESP – São Paulo State University
