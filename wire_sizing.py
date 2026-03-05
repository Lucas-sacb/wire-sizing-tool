"""
Wire sizing tool for high-power electric propulsion systems.

Features
--------
• AWG sizing based on:
    - RMS current
    - voltage drop
    - current density

• Electrical loss analysis
• Wire mass estimation
• Thermal equilibrium estimation
• Safety evaluation

Author: Lucas
"""

from dataclasses import dataclass
from typing import Dict, List
import math
import matplotlib.pyplot as plt


# ==================================================
# PHYSICAL CONSTANTS
# ==================================================

COPPER_RESISTIVITY = 1.68e-8          # Ohm*m
COPPER_DENSITY = 8960                 # kg/m³

MAX_CURRENT_DENSITY = 20              # A/mm²

AMBIENT_TEMP = 25                     # °C
WIRE_TEMP_LIMIT = 270                 # °C (silicone insulation)

CONVECTION_COEFF = 35                 # W/(m²*K)


# ==================================================
# DATA STRUCTURES
# ==================================================

@dataclass
class AWGSpec:
    """Electrical properties of an AWG wire."""
    area_mm2: float
    ampacity: float


@dataclass
class AWGAnalysis:
    """Results for a specific AWG gauge."""
    awg: int
    power_loss: float
    mass: float
    efficiency: float
    temperature: float
    safe: bool


@dataclass
class SizingResult:
    """Recommended AWG result."""
    awg: int
    peak_current: float
    rms_current: float
    min_required_area: float


# ==================================================
# AWG DATABASE
# ==================================================

AWG_TABLE: Dict[int, AWGSpec] = {
    4: AWGSpec(21.15, 300),
    6: AWGSpec(13.30, 220),
    8: AWGSpec(8.37, 180),
    10: AWGSpec(5.26, 140),
    12: AWGSpec(3.31, 90),
    14: AWGSpec(2.08, 60),
    16: AWGSpec(1.31, 40),
    18: AWGSpec(0.82, 25),
    20: AWGSpec(0.52, 15),
}


# ==================================================
# ELECTRICAL MODEL
# ==================================================

def rms_current(i_peak: float, i_cruise: float, t_peak: float, t_total: float) -> float:
    """
    Compute RMS current based on mission profile.
    """
    return math.sqrt(
        (i_peak**2 * t_peak + i_cruise**2 * (t_total - t_peak)) / t_total
    )


def wire_resistance(length: float, area_m2: float) -> float:
    """
    Compute electrical resistance of the wire.
    """
    return COPPER_RESISTIVITY * length / area_m2


def wire_temperature(power_loss: float, diameter: float, length: float) -> float:
    """
    Estimate steady-state wire temperature.
    """
    surface_area = math.pi * diameter * length
    return AMBIENT_TEMP + power_loss / (CONVECTION_COEFF * surface_area)


# ==================================================
# SIZING ALGORITHM
# ==================================================

def size_wire(
    power: float,
    voltage: float,
    length: float,
    t_peak: float,
    t_total: float,
    cruise_fraction: float = 0.6,
    voltage_drop_limit: float = 0.02,
    safety_factor: float = 1.25,
) -> SizingResult:
    """
    Determine minimum AWG that satisfies electrical and thermal constraints.
    """

    i_peak = power / voltage
    i_cruise = cruise_fraction * i_peak

    i_rms = rms_current(i_peak, i_cruise, t_peak, t_total)
    i_rms *= safety_factor

    total_length = 2 * length

    delta_v = voltage * voltage_drop_limit

    area_voltage = (COPPER_RESISTIVITY * total_length * i_peak) / delta_v
    area_voltage *= 1e6

    area_thermal = i_rms / MAX_CURRENT_DENSITY

    required_area = max(area_voltage, area_thermal)

    for awg in sorted(AWG_TABLE.keys(), reverse=True):

        spec = AWG_TABLE[awg]

        if spec.area_mm2 >= required_area and spec.ampacity >= i_rms:

            return SizingResult(
                awg=awg,
                peak_current=i_peak,
                rms_current=i_rms,
                min_required_area=required_area,
            )

    raise ValueError("No AWG in table satisfies the constraints.")


# ==================================================
# AWG PERFORMANCE ANALYSIS
# ==================================================

def analyze_awg_options(power: float, voltage: float, length: float) -> List[AWGAnalysis]:
    """
    Compute performance metrics for each AWG.
    """

    current = power / voltage
    total_length = 2 * length

    results: List[AWGAnalysis] = []

    for awg, spec in AWG_TABLE.items():

        area_m2 = spec.area_mm2 * 1e-6

        resistance = wire_resistance(total_length, area_m2)

        power_loss = current**2 * resistance

        efficiency = power / (power + power_loss)

        volume = area_m2 * total_length
        mass = COPPER_DENSITY * volume

        diameter = math.sqrt(4 * area_m2 / math.pi)

        temp = wire_temperature(power_loss, diameter, total_length)

        safe = temp < WIRE_TEMP_LIMIT

        results.append(
            AWGAnalysis(
                awg=awg,
                power_loss=power_loss,
                mass=mass,
                efficiency=efficiency,
                temperature=temp,
                safe=safe,
            )
        )

    return results


# ==================================================
# VISUALIZATION
# ==================================================

def plot_losses(results: List[AWGAnalysis]) -> None:
    """
    Plot AWG vs electrical losses.
    """

    awg = [r.awg for r in results]
    losses = [r.power_loss for r in results]

    plt.figure()

    plt.plot(awg, losses, marker="o")

    plt.gca().invert_xaxis()

    plt.xlabel("AWG")
    plt.ylabel("Power Loss [W]")

    plt.title("Wire Electrical Loss vs Gauge")

    plt.grid(True)

    plt.show()


# ==================================================
# CLI INTERFACE
# ==================================================

def main():

    power = float(input("Motor peak power [W]: "))
    voltage = float(input("Battery voltage [V]: "))
    length = float(input("Wire length (one direction) [m]: "))
    t_peak = float(input("Takeoff time [s]: "))
    t_total = float(input("Total flight time [s]: "))

    sizing = size_wire(power, voltage, length, t_peak, t_total)

    print("\nRecommended wire:\n")

    print(f"AWG: {sizing.awg}")
    print(f"Peak current: {sizing.peak_current:.2f} A")
    print(f"RMS current: {sizing.rms_current:.2f} A")
    print(f"Minimum area required: {sizing.min_required_area:.2f} mm²")

    results = analyze_awg_options(power, voltage, length)

    print("\nAWG analysis:\n")

    for r in results:

        status = "SAFE" if r.safe else "NOT SAFE"

        print(
            f"AWG {r.awg:>2} | "
            f"Loss = {r.power_loss:6.2f} W | "
            f"Mass = {r.mass*1000:6.1f} g | "
            f"Efficiency = {r.efficiency*100:5.2f}% | "
            f"Temp = {r.temperature:6.1f} °C | "
            f"{status}"
        )

    plot_losses(results)


# ==================================================

if __name__ == "__main__":
    main()
