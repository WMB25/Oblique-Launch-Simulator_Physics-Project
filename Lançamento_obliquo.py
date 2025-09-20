import sys, os, csv, math

print("Lançamento oblíquo\n")

gravity = 9.81 
velocity = float(input("Digite a velocidade inicial (m/s): "))
angle = float(input("Digite o ângulo de lançamento (graus): "))
time_step = float(input("Digite o intervalo de tempo para cálculo (s): "))

def launch_oblique(velocity, angle, time_step):
    angle_rad = math.radians(angle)
    time_of_flight = (2 * velocity * math.sin(angle_rad)) / gravity

    positions = []
    time = 0
    while time <= time_of_flight:
        pos_x = velocity * math.cos(angle_rad) * time
        pos_y = (velocity * math.sin(angle_rad) * time) - (0.5 * gravity * time**2)
        positions.append((time, pos_x, pos_y))
        time += time_step
    if positions[-1][0] < time_of_flight:
        time = time_of_flight
        pos_x = velocity * math.cos(angle_rad) * time
        pos_y = (velocity * math.sin(angle_rad) * time) - (0.5 * gravity * time**2)
        positions.append((time, pos_x, pos_y))
    return positions

positions = launch_oblique(velocity, angle, time_step)

with open("lancamento_obliquo.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tempo (s)", "Posição X (m)", "Posição Y (m)"])

    for point in positions:
        writer.writerow([round(point[0], 3), round(point[1], 3), round(point[2], 3)])

    print("Dados salvos em 'lancamento_obliquo.csv'")