import math
import json
import os

def perform_vd_analysis(data):
    steps = []
    
   
    PEC_TABLE_DATA = {
        '2.0':  {'xl': {'PVC': 0.058, 'Steel': 0.073}, 'r': {'Copper': {'PVC': 3.1, 'Alum': 3.1, 'Steel': 3.1}, 'Aluminum': {'PVC': 5.1, 'Alum': 5.1, 'Steel': 5.1}}},
        '3.5':  {'xl': {'PVC': 0.054, 'Steel': 0.068}, 'r': {'Copper': {'PVC': 2.0, 'Alum': 2.0, 'Steel': 2.0}, 'Aluminum': {'PVC': 3.2, 'Alum': 3.2, 'Steel': 3.2}}},
        '5.5':  {'xl': {'PVC': 0.050, 'Steel': 0.063}, 'r': {'Copper': {'PVC': 1.2, 'Alum': 1.2, 'Steel': 1.2}, 'Aluminum': {'PVC': 2.0, 'Alum': 2.0, 'Steel': 2.0}}},
        '8.0':  {'xl': {'PVC': 0.052, 'Steel': 0.065}, 'r': {'Copper': {'PVC': 0.78, 'Alum': 0.78, 'Steel': 0.78}, 'Aluminum': {'PVC': 1.3, 'Alum': 1.3, 'Steel': 1.3}}},
        '14':   {'xl': {'PVC': 0.051, 'Steel': 0.064}, 'r': {'Copper': {'PVC': 0.49, 'Alum': 0.49, 'Steel': 0.49}, 'Aluminum': {'PVC': 0.81, 'Alum': 0.81, 'Steel': 0.81}}},
        '22':   {'xl': {'PVC': 0.048, 'Steel': 0.060}, 'r': {'Copper': {'PVC': 0.31, 'Alum': 0.31, 'Steel': 0.31}, 'Aluminum': {'PVC': 0.51, 'Alum': 0.51, 'Steel': 0.51}}},
        '30':   {'xl': {'PVC': 0.045, 'Steel': 0.057}, 'r': {'Copper': {'PVC': 0.19, 'Alum': 0.20, 'Steel': 0.20}, 'Aluminum': {'PVC': 0.32, 'Alum': 0.32, 'Steel': 0.32}}},
        '38':   {'xl': {'PVC': 0.046, 'Steel': 0.057}, 'r': {'Copper': {'PVC': 0.15, 'Alum': 0.16, 'Steel': 0.16}, 'Aluminum': {'PVC': 0.25, 'Alum': 0.26, 'Steel': 0.25}}},
        '50':   {'xl': {'PVC': 0.044, 'Steel': 0.055}, 'r': {'Copper': {'PVC': 0.12, 'Alum': 0.13, 'Steel': 0.12}, 'Aluminum': {'PVC': 0.20, 'Alum': 0.21, 'Steel': 0.20}}},
        '60':   {'xl': {'PVC': 0.043, 'Steel': 0.054}, 'r': {'Copper': {'PVC': 0.10, 'Alum': 0.10, 'Steel': 0.10}, 'Aluminum': {'PVC': 0.16, 'Alum': 0.16, 'Steel': 0.16}}},
        '80':   {'xl': {'PVC': 0.042, 'Steel': 0.052}, 'r': {'Copper': {'PVC': 0.077, 'Alum': 0.082, 'Steel': 0.079}, 'Aluminum': {'PVC': 0.13, 'Alum': 0.13, 'Steel': 0.13}}},
        '100':  {'xl': {'PVC': 0.041, 'Steel': 0.051}, 'r': {'Copper': {'PVC': 0.062, 'Alum': 0.067, 'Steel': 0.063}, 'Aluminum': {'PVC': 0.10, 'Alum': 0.11, 'Steel': 0.10}}},
        '125':  {'xl': {'PVC': 0.041, 'Steel': 0.052}, 'r': {'Copper': {'PVC': 0.052, 'Alum': 0.057, 'Steel': 0.054}, 'Aluminum': {'PVC': 0.085, 'Alum': 0.090, 'Steel': 0.086}}},
        '150':  {'xl': {'PVC': 0.041, 'Steel': 0.051}, 'r': {'Copper': {'PVC': 0.044, 'Alum': 0.049, 'Steel': 0.045}, 'Aluminum': {'PVC': 0.071, 'Alum': 0.076, 'Steel': 0.072}}},
        '175':  {'xl': {'PVC': 0.040, 'Steel': 0.050}, 'r': {'Copper': {'PVC': 0.038, 'Alum': 0.043, 'Steel': 0.039}, 'Aluminum': {'PVC': 0.061, 'Alum': 0.066, 'Steel': 0.063}}},
        '200':  {'xl': {'PVC': 0.040, 'Steel': 0.049}, 'r': {'Copper': {'PVC': 0.033, 'Alum': 0.038, 'Steel': 0.035}, 'Aluminum': {'PVC': 0.054, 'Alum': 0.059, 'Steel': 0.055}}},
        '250':  {'xl': {'PVC': 0.039, 'Steel': 0.048}, 'r': {'Copper': {'PVC': 0.027, 'Alum': 0.032, 'Steel': 0.029}, 'Aluminum': {'PVC': 0.043, 'Alum': 0.048, 'Steel': 0.045}}},
        '325':  {'xl': {'PVC': 0.039, 'Steel': 0.048}, 'r': {'Copper': {'PVC': 0.023, 'Alum': 0.028, 'Steel': 0.025}, 'Aluminum': {'PVC': 0.036, 'Alum': 0.041, 'Steel': 0.038}}},
        '375':  {'xl': {'PVC': 0.038, 'Steel': 0.048}, 'r': {'Copper': {'PVC': 0.019, 'Alum': 0.024, 'Steel': 0.021}, 'Aluminum': {'PVC': 0.029, 'Alum': 0.034, 'Steel': 0.031}}},
        '400':  {'xl': {'PVC': 0.038, 'Steel': 0.048}, 'r': {'Copper': {'PVC': 0.019, 'Alum': 0.024, 'Steel': 0.021}, 'Aluminum': {'PVC': 0.029, 'Alum': 0.034, 'Steel': 0.031}}},
        '500':  {'xl': {'PVC': 0.037, 'Steel': 0.046}, 'r': {'Copper': {'PVC': 0.015, 'Alum': 0.019, 'Steel': 0.018}, 'Aluminum': {'PVC': 0.023, 'Alum': 0.027, 'Steel': 0.025}}},
    }


    v_send = float(data.get('voltage', 230))
    I = float(data.get('load_current', 0))
    L = float(data.get('distance', 0))
    n = int(data.get('n_parallel', 1))
    t_operating = float(data.get('temp_conductor', 75))
    material = data.get('material', 'Copper')
    wire_size = str(data.get('wire_size', '125'))
    install_method = data.get('installation', 'PVC Conduit')


    xl_key = 'Steel' if 'Steel' in install_method else 'PVC'
    r_key = 'Steel' if 'Steel' in install_method else ('Alum' if 'Aluminum' in install_method else 'PVC')
    size_data = PEC_TABLE_DATA.get(wire_size, PEC_TABLE_DATA['125'])
    r_val = size_data['r'][material][r_key]
    x_val = size_data['xl'][xl_key]

  
    a_const = 1.732 if data.get('system_type') == "Three Phase" else 2.0
    z_mag = math.sqrt(r_val**2 + x_val**2)
    numerator = a_const * I * L * z_mag
    
 
    vd_at_t_operating = round(numerator / (n * 305), 3)

    alpha = 0.00386 if material == 'Copper' else 0.00429
    
 
    multiplier_t_operating = 1 + (alpha * (t_operating - 20))
    multiplier_75 = 1 + (alpha * (75 - 20))
    
    vd_20 = round(vd_at_t_operating / multiplier_t_operating, 3)
    vd_75 = round(vd_20 * multiplier_75, 3)


    steps.append(f"LOCATION: [ {data.get('location', 'NOT SPECIFIED').upper()} ]")
    steps.append(f"VOLTAGE DROP (VD) = ({a_const} X {I} X {L} X √({r_val}² + {x_val}²)) / ({n} X 305)")
    steps.append(f"VOLTAGE DROP (VD) = {round(numerator, 4)} / 305")
    steps.append(f"VOLTAGE DROP (VP) = {vd_at_t_operating} V")

    steps.append("")
    steps.append("CONSIDERING TEMPERATURE EFFECTS:")
    steps.append(f"VD_R@75°C = VD_R@20°C (1 + α@20°C (T_75°C - T_20°C))")
    steps.append(f"{vd_75} = VD_R@20°C (1 + {alpha} X (75 - 20))")
    steps.append(f"VD_R@20°C = {vd_20}")
    steps.append(f"VD_R@T2°C = {vd_20} (1 + {alpha} X ({t_operating} - 20))")
    steps.append(f"VD_R@T2°C = {vd_at_t_operating} V")


    v_receive = round(v_send - vd_at_t_operating, 3)
    vd_percent = round((vd_at_t_operating / v_send) * 100, 3)
    
    steps.append("")
    steps.append(f"RECEIVING VOLTAGE = {v_send} - {vd_at_t_operating} = {v_receive} V")
    steps.append(f"%VD = ({vd_at_t_operating} / {v_send}) X 100 = {vd_percent} %")

    return {
        "vd_val": vd_at_t_operating,
        "receiving_voltage": v_receive,
        "percentage": vd_percent,
        "solution_steps": steps
    }