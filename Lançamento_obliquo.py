import sys, os, csv, math

print("Lançamento oblíquo\n")

GRAVITY = 9.81 
MASS = 2.72
AREA = math.pi * (0.1)**2
DRAG_COEFFICIENT = 0.47
AIR_DENSITY = 1.225

velocity = float(input("Digite a velocidade inicial (m/s): "))
angle = math.radians(float(input("Digite o ângulo de lançamento (graus): ")))
time_step = float(input("Digite o intervalo de tempo para cálculo (s): "))
mech_force_magnitude = float(input("Digite a força mecânica (N): "))
mech_force_angle = math.radians(float(input("Digite o ângulo da força mecânica (graus): ")))

def launch_oblique(velocity, angle, time_step, mech_force_magnitude, mech_force_angle):
    x, y, time = 0.0, 0.0, 0.0

    velocity_x = velocity * math.cos(angle)
    velocity_y = velocity * math.sin(angle)
    mech_force_x = mech_force_magnitude * math.cos(mech_force_angle)
    mech_force_y = mech_force_magnitude * math.sin(mech_force_angle)

    positions = []

    while y >= 0:
        velocity_total = math.sqrt((velocity_x**2) + (velocity_y**2))
        drag_force = 0.5 * AIR_DENSITY * velocity_total**2 * AREA * DRAG_COEFFICIENT

        if(velocity_total > 0):
            drag_acelaration_x = - (drag_force / MASS) * (velocity_x / velocity_total)
            drag_acelaration_y = - (drag_force / MASS) * (velocity_y / velocity_total)
        else:
            drag_acelaration_x = 0
            drag_acelaration_y = 0

        mech_acceleration_x = mech_force_x / MASS
        mech_acceleration_y = mech_force_y / MASS

        acceleration_x = drag_acelaration_x + mech_acceleration_x
        acceleration_y = -GRAVITY + drag_acelaration_y + mech_acceleration_y

        velocity_x += acceleration_x * time_step
        velocity_y += acceleration_y * time_step
        x += velocity_x * time_step
        y += velocity_y * time_step

        positions.append((
            time, x, y,
            velocity_x, velocity_y, velocity_total,
            acceleration_x, acceleration_y,
            drag_force, mech_force_x, mech_force_y
            ))
        
        time += time_step
        if time > 1000:
            break
        
    return positions

positions = launch_oblique(velocity, angle, time_step, mech_force_magnitude, mech_force_angle)

print(f"\nDados do lançamento:")
print(f"Massa: {MASS} kg")
print(f"Área: {AREA} m²")
print(f"Coeficiente de arrasto: {DRAG_COEFFICIENT}")
print(f"Densidade do ar: {AIR_DENSITY} kg/m³")
print(f"Gravidade: {GRAVITY} m/s²")
print(f"Força Mecânica: {mech_force_magnitude} N")
print(f"Ângulo da Força Mecânica: {math.degrees(mech_force_angle):.1f}º\n")

simulation_params = {
    "Velocidade Inicial": f"{velocity} m/s",
    "Ângulo de Lançamento": f"{math.degrees(angle):.1f}°",
    "Massa": f"{MASS} kg",
    "Gravidade": f"{GRAVITY} m/s²",
    "Força Mecânica": f"{mech_force_magnitude} N",
    "Ângulo da Força": f"{math.degrees(mech_force_angle):.1f}°"
}

with open("lancamento_obliquo.csv", "w", newline='', encoding='utf-8') as file:
    file.write("# SIMULAÇÃO DE LANÇAMENTO OBLÍQUO\n")
    file.write("# Parâmetros da simulação:\n")
    for key, value in simulation_params.items():
        file.write(f"# {key}: {value}\n")
    file.write("#\n")
    
    fieldnames = [
        "tempo_s", "posicao_x_m", "posicao_y_m", 
        "velocidade_x_ms", "velocidade_y_ms", "velocidade_total_ms",
        "aceleracao_x_ms2", "aceleracao_y_ms2", 
        "forca_arrasto_n", "forca_mecanica_x_n", "forca_mecanica_y_n"
    ]
    
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    
    for point in positions:
        writer.writerow({
            "tempo_s": round(point[0], 4),
            "posicao_x_m": round(point[1], 4),
            "posicao_y_m": round(point[2], 4),
            "velocidade_x_ms": round(point[3], 4),
            "velocidade_y_ms": round(point[4], 4),
            "velocidade_total_ms": round(point[5], 4),
            "aceleracao_x_ms2": round(point[6], 4),
            "aceleracao_y_ms2": round(point[7], 4),
            "forca_arrasto_n": round(point[8], 4),
            "forca_mecanica_x_n": round(point[9], 4),
            "forca_mecanica_y_n": round(point[10], 4)
        })
        
print("Dados salvos organizadamente em 'lancamento_obliquo.csv'")