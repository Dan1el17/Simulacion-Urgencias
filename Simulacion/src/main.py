#!/usr/bin/env python3
"""
Modelado y Análisis de un Servicio de Emergencias Hospitalarias
mediante Redes de Colas Abiertas para la Identificación de Cuellos
de Botella y Optimización de Personal

Autores: Flores Gallardo Emilio Josue, Pardo Lima Steeven Daniel,
         Vega Jimenez Servio Julian, Valarezo Roman Maria del Cisne
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import load_parameters
from experiments import run_full_experiment, find_min_stable_staffing
from visualization import (
    plot_utilization_by_stage,
    plot_wait_vs_doctors,
    plot_wait_by_gravity,
    create_results_tables,
    print_all_console_tables
)


def get_scenario_field(scenario, field):
    """Obtiene un campo del escenario funcionando con dict o con objeto."""
    if isinstance(scenario, dict):
        return scenario[field]
    return getattr(scenario, field)


def main():
    print("=" * 70)
    print("MODELADO DE SERVICIO DE EMERGENCIAS - REDES DE COLAS DE JACKSON")
    print("=" * 70)

    # Permite pasar un config opcional: python -m src.main config/quick_parameters.yaml
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config/base_parameters.yaml"
    params = load_parameters(config_path)
    print(f"\nConfiguracion cargada: {params.simulation.replications} replicas, "
          f"{params.simulation.horizon_hours}h horizonte, "
          f"{params.simulation.warmup_hours}h warm-up")

    print("\n" + "=" * 70)
    print("EJECUTANDO EXPERIMENTO COMPLETO")
    print("=" * 70)

    result = run_full_experiment(params)

    print("\n" + "=" * 70)
    print("BÚSQUEDA DE PERSONAL MÍNIMO ESTABLE")
    print("=" * 70)

    min_staff = find_min_stable_staffing(result.analytical_results, max_W_system=120)
    if min_staff["found"]:
        print(f"\nConfiguracion minima estable (W < 120 min):")
        print(f"  Medicos (c3): {min_staff['c3']}")
        print(f"  Enfermeros (c5): {min_staff['c5']}")
        print(f"  Tiempo en sistema: {min_staff['W_system_min']:.1f} min")
        print(f"  Cuello de botella: {min_staff['bottleneck']}")
    else:
        print(f"\n{min_staff['message']}")

    if result.analytical_results:
        print("\n" + "=" * 70)
        print("GENERANDO GRAFICAS (un juego completo por escenario)")
        print("=" * 70)

        os.makedirs("output", exist_ok=True)

        # Lista de escenarios seleccionados: saturado / equilibrado / holgado
        scenarios = []
        for sc in params.parameter_sweep.selected_scenarios:
            scenarios.append({
                "c3": get_scenario_field(sc, "c3"),
                "c5": get_scenario_field(sc, "c5"),
                "label": get_scenario_field(sc, "label")
            })

        # Respaldo: si el config no define escenarios, usa el primer resultado
        if not scenarios:
            first = result.analytical_results[0]
            scenarios = [{"c3": first["c3"], "c5": first["c5"], "label": "base"}]

        total_graficas = 0

        # ============================================================
        # GRAFICA 1: Utilizacion por etapa (UNA POR CADA ESCENARIO)
        # ============================================================
        print("\n--- Grafica 1: Utilizacion por etapa ---")
        for sc in scenarios:
            safe_label = str(sc["label"]).replace(" ", "_")
            path = f"output/grafica_utilizacion_{safe_label}.png"
            print(f"  -> {sc['label']} (c3={sc['c3']}, c5={sc['c5']}): {path}")
            plot_utilization_by_stage(
                result.analytical_results, sc["c3"], sc["c5"],
                save_path=path, scenario_label=sc["label"]
            )
            total_graficas += 1

        # ============================================================
        # GRAFICA 2: Espera vs. medicos (UNA POR CADA ESCENARIO)
        # ============================================================
        print("\n--- Grafica 2: Espera vs. numero de medicos ---")
        for sc in scenarios:
            safe_label = str(sc["label"]).replace(" ", "_")
            path = f"output/grafica_espera_vs_medicos_{safe_label}.png"
            print(f"  -> {sc['label']} (c5={sc['c5']} fijo, destacando c3={sc['c3']}): {path}")
            plot_wait_vs_doctors(
                result.analytical_results, fixed_c5=sc["c5"],
                save_path=path, scenario_label=sc["label"],
                highlight_c3=sc["c3"]
            )
            total_graficas += 1

        # ============================================================
        # GRAFICA 3: Espera por gravedad, FIFO vs prioridad
        #            (UNA POR CADA ESCENARIO)
        # ============================================================
        print("\n--- Grafica 3: Espera por gravedad (con vs. sin prioridad) ---")
        for label, pri in result.priority_results.items():
            safe_label = str(label).replace(" ", "_")
            path = f"output/grafica_espera_gravedad_{safe_label}.png"
            print(f"  -> {label}: {path}")
            plot_wait_by_gravity(pri, label, save_path=path)
            total_graficas += 1

        print(f"\nTOTAL DE GRAFICAS GENERADAS: {total_graficas} (carpeta output/)")

    print("\n" + "=" * 70)
    print("MOSTRANDO RESULTADOS EN CONSOLA")
    print("=" * 70)

    print_all_console_tables(
        result.analytical_results,
        result.validation_results,
        result.priority_results,
        params.parameter_sweep.selected_scenarios
    )

    print("\n" + "=" * 70)
    print("GUARDANDO TABLAS EN CSV (carpeta output/)")
    print("=" * 70)

    create_results_tables(
        result.analytical_results,
        result.validation_results,
        result.priority_results,
        output_dir="output"
    )

    print("\n" + "=" * 70)
    print("EXPERIMENTO COMPLETADO EXITOSAMENTE")
    print("=" * 70)


if __name__ == "__main__":
    main()
    