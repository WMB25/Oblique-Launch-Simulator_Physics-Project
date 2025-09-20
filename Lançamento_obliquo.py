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

def launch_oblique(velocity, angle, time_step):
    x, y, time = 0.0, 0.0, 0.0

    velocity_x = velocity * math.cos(angle)
    velocity_y = velocity * math.sin(angle)
    
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

        acceleration_x = drag_acelaration_x
        acceleration_y = -GRAVITY + drag_acelaration_y

        velocity_x += acceleration_x * time_step
        velocity_y += acceleration_y * time_step
        x += velocity_x * time_step
        y += velocity_y * time_step

        positions.append((time, x, y))
        time += time_step

        if time > 1000:
            break
    return positions

positions = launch_oblique(velocity, angle, time_step)

print(f"\nDados do lançamento:")
print(f"Massa: {MASS} kg")
print(f"Área: {AREA} m²")
print(f"Coeficiente de arrasto: {DRAG_COEFFICIENT}")
print(f"Densidade do ar: {AIR_DENSITY} kg/m³")
print(f"Gravidade: {GRAVITY} m/s²\n")

with open("lancamento_obliquo.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tempo (s)", "Posição X (m)", "Posição Y (m)"])

    for point in positions:
        writer.writerow([round(point[0], 3), round(point[1], 3), round(point[2], 3)])
    print("Dados salvos em 'lancamento_obliquo.csv'")