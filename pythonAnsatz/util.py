import numpy as np
import pythreejs as three
import time
from scipy.spatial.transform import Rotation as R, Slerp


def quaternion_to_euler(x, y, z, w, order):
    quaternion = [x, y, z, w]
    euler_angles = R.from_quat(quaternion).as_euler(order, degrees=True)
    return euler_angles


#??
def euler_to_rot_mat(x, y, z, order):
    euler_angles = [x,y,z]
    r = R.from_euler(order, euler_angles, degrees=True)
    return r.as_matrix()

#??
def rot_matrix_to_euler(rot_mat, order):
    r = R.from_matrix(rot_mat)
    return r.as_euler(order, degrees=True)

def rot_matrix_to_quaternion(rot_mat):
    r = R.from_matrix(rot_mat).as_quat()
    return r

#??
def euler_to_quaternion(x, y, z, order='XYZ'):
    angles = [x,y,z]
    r = R.from_euler(order, angles, degrees=True)
    quat = r.as_quat()
    return quat


def compute_normals(vertices, indices):
    # Initialisiere Array für Normalen
    normals = np.zeros_like(vertices)

    # Für jedes Dreieck die Flächennormale berechnen
    for i in range(0, len(indices), 3):
        idx1, idx2, idx3 = indices[i], indices[i+1], indices[i+2]
        v1, v2, v3 = vertices[idx1], vertices[idx2], vertices[idx3]

        # Berechne zwei Kanten des Dreiecks
        edge1 = v2 - v1
        edge2 = v3 - v1

        # Kreuzprodukt für die Flächennormale
        face_normal = np.cross(edge1, edge2)

        # Normalisiere die Flächennormale
        face_normal = face_normal / np.linalg.norm(face_normal)

        # Addiere die Flächennormale zu den Vertex-Normalen
        normals[idx1] += face_normal
        normals[idx2] += face_normal
        normals[idx3] += face_normal

    # Normalisiere die Vertex-Normalen
    normals = np.array([n / np.linalg.norm(n) if np.linalg.norm(n) > 0 else n for n in normals])
    return normals




def quaternion_multiply(q1, q2):
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2
    
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    
    return [x, y, z, w]








def create_axes(len):
    line_material_x = three.LineBasicMaterial(color='red')
    line_material_y = three.LineBasicMaterial(color='green')
    line_material_z = three.LineBasicMaterial(color='blue')

    points_x = [[0,0,0], [len,0,0]]
    points_y = [[0,0,0], [0,len,0]]
    points_z = [[0,0,0], [0,0,len]]

    line_geometry_x = three.BufferGeometry(attributes={'position' : three.BufferAttribute(points_x, False)})
    line_geometry_y = three.BufferGeometry(attributes={'position' : three.BufferAttribute(points_y, False)})
    line_geometry_z = three.BufferGeometry(attributes={'position' : three.BufferAttribute(points_z, False)})

    line_x = three.Line(line_geometry_x, line_material_x)
    line_y = three.Line(line_geometry_y, line_material_y)
    line_z = three.Line(line_geometry_z, line_material_z)

    axes_group = three.Group()
    axes_group.add(line_x)
    axes_group.add(line_y)
    axes_group.add(line_z)
    return axes_group







def create_grid(size, density):
    line_material = three.LineBasicMaterial(color='#777777')
    line_material.transparent = True
    line_material.opacity = 0.5

    grid_group = three.Group()
    for i in range((int)((-size/2)*(1/density)), (int)((size/2)*(1/density))+1):
        points1 = [[-size/2,i*density,0],[size/2,i*density,0]]
        points2 = [[i*density,-size/2,0],[i*density,size/2,0]]
        # Geometrie für die Linie
        line_geometry1 = three.BufferGeometry(
        attributes={'position': three.BufferAttribute(points1, False)})
        line1 = three.Line(line_geometry1, line_material)
        line_geometry2 = three.BufferGeometry(
        attributes={'position': three.BufferAttribute(points2, False)})
        line2 = three.Line(line_geometry2, line_material)
        grid_group.add(line1)
        grid_group.add(line2)

    return grid_group




def apply_rot_matrix(mesh, rot_mat):
    # Konvertiere Matrix in Quaternion
    r = R.from_matrix(rot_mat)
    q = r.as_quat()  # Reihenfolge: [x, y, z, w]

    # Setze Quaternion (pythreejs erwartet [w, x, y, z])
    mesh.quaternion = quaternion_multiply((q[0], q[1], q[2], q[3]), mesh.quaternion)






def createQuad(posX, posY, posZ, width, height, depth, r=0, g=255, b=0):
    # Erstelle die Geometrie (Breite, Höhe, Tiefe)
    geometry = three.BoxGeometry(width=width, height=height, depth=depth)
    # Material (Farbe & Eigenschaften)
    hex_color = f'#{r:02X}{g:02X}{b:02X}'
    material = three.MeshStandardMaterial(color=hex_color, metalness=0.5, roughness=0.8, transparent=True, opacity=0.5, depthWrite=False)
    # Erstelle das Mesh (Geometrie + Material)
    mesh = three.Mesh(geometry, material)
    mesh.position = (posX, posY, posZ)
    return mesh






def apply_rot_matrix_animated(mesh, rot_mat):
    q = R.from_matrix(rot_mat).as_quat() 
    old_quat = mesh.quaternion
    new_quat = quaternion_multiply(mesh.quaternion, (q[0], q[1], q[2], q[3]))
    t = 0
    delta = 0.002
    while(t <= 1):
        n = slerp_quaternion(old_quat, new_quat, t)
        mesh.quaternion = [n[0], n[1], n[2], n[3]]
        t += delta
        time.sleep(0.01)




def slerp_quaternion(q1, q2, t):
    if not (0.0 <= t <= 1.0):
        raise ValueError("Der Interpolationswert t muss zwischen 0 und 1 liegen.")
    
    # Erstelle Rotationsobjekte
    key_times = np.array([0, 1])  # Start (0) und Ende (1)
    key_rots = R.from_quat([q1, q2])  # Quaternionen als Rotation-Objekte

    # SLERP-Interpolation erstellen
    slerp = Slerp(key_times, key_rots)

    # Interpolierte Rotation abrufen
    interpolated_rotation = slerp(t)

    return interpolated_rotation.as_quat()









def set_scale(mesh, x, y, z):
    mesh.scale = (x, y, z)
    

def set_scale_animated(mesh, x, y, z):
    old_x = mesh.scale[0]
    old_y = mesh.scale[1]
    old_z = mesh.scale[2]
    t = 0
    delta = 0.02
    while(t<=1):
        current_x = (x-old_x)*t + old_x
        current_y = (y-old_y)*t + old_y
        current_z = (z-old_z)*t + old_z
        mesh.scale = (current_x, current_y, current_z)
        t+=delta
        time.sleep(0.01)



def rotate_animated(mesh, x, y, z, order):
    time.sleep(0.5)
    if order == "XYZ":
        delta = 0.5
        if np.deg2rad(x) < 0:
            delta *= -1
        counter = delta
        while counter < abs(x):
            q = euler_to_quaternion(delta, 0, 0, order)
            mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
            counter+=abs(delta)
            time.sleep(0.01)
        time.sleep(0.5)
        delta = 0.5
        if y < 0:
            delta *= -1
        counter = delta
        while counter < abs(y):
            q = euler_to_quaternion(0, delta, 0, order)
            mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
            counter+=abs(delta)
            time.sleep(0.01)
        time.sleep(0.5)
        delta = 0.5
        if z < 0:
            delta *= -1
        counter = delta
        while counter < abs(z):
            q = euler_to_quaternion(0, 0, delta, order)
            mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
            counter+=abs(delta)
            time.sleep(0.01)
        time.sleep(0.5)
    elif order == "XZY":
        delta = 0.5
        if x < 0:
            delta *= -1
        counter = delta
        while counter < abs(x):
            q = euler_to_quaternion(delta, 0, 0, order)
            mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
            counter+=abs(delta)
            time.sleep(0.01)
        time.sleep(0.5)
        delta = 0.5
        if np.deg2rad(z) < 0:
            delta *= -1
        counter = delta
        while counter < abs(z):
            q = euler_to_quaternion(0, 0, delta, order)
            mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
            counter+=abs(delta)
            time.sleep(0.01)
        time.sleep(0.5)
        delta = 0.5
        if y < 0:
            delta *= -1
        counter = delta
        while counter < abs(y):
            q = euler_to_quaternion(0, delta, 0, order)
            mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
            counter+=abs(delta)
            time.sleep(0.01)
        time.sleep(0.5)
    elif order == "YXZ":
        delta = 0.5
        if y < 0:
            delta *= -1
        counter = delta
        while counter < abs(y):
            q = euler_to_quaternion(0, delta, 0, order)
            mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
            counter+=abs(delta)
            time.sleep(0.01)
        time.sleep(0.5)
        delta = 0.5
        if x < 0:
            delta *= -1
        counter = delta
        while counter < abs(x):
            q = euler_to_quaternion(delta, 0, 0, order)
            mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
            counter+=abs(delta)
            time.sleep(0.01)
        time.sleep(0.5)
        delta = 0.5
        if z < 0:
            delta *= -1
        counter = delta
        while counter < abs(z):
            q = euler_to_quaternion(0, 0, delta, order)
            mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
            counter+=abs(delta)
            time.sleep(0.01)
        time.sleep(0.5)





def rotate_world(obj, angles, order='XYZ'):
    """
    Wendet eine Rotation um das Welt-Koordinatensystem an.
    :param obj: Das 3D-Objekt (Mesh)
    :param angles: Die Euler-Winkel [x, y, z] in Grad
    :param order: Die Rotationsreihenfolge (z. B. 'XYZ', 'ZYX')
    """
    # Erstelle eine Rotation aus den Euler-Winkeln
    r = R.from_euler(order, angles, degrees=True)

    # Wandle die Rotation in ein Quaternion um
    q_new = r.as_quat()  # [x, y, z, w]

    # Wandle das bestehende Quaternion des Objekts in ein NumPy-Array um
    q_current = np.array(obj.quaternion)  # [x, y, z, w]

    # Quaternion-Multiplikation (neue Rotation zuerst!)
    q_result = R.from_quat(q_new) * R.from_quat(q_current)

    # Setze das neue Quaternion am Objekt
    obj.quaternion = list(q_result.as_quat())




def rotate(mesh, x, y, z, order):
    q = euler_to_quaternion(x, y, z, order)
    mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
    print(mesh.quaternion)

def set_rotation(mesh, x, y, z, order):
    q = euler_to_quaternion(x, y, z, order=order)
    mesh.quaternion = [q[0], q[1], q[2], q[3]]

def translate(mesh, x=0, y=0, z=0):
    mesh.position = (mesh.position[0]+x, mesh.position[1]+y, mesh.position[2]+z)

def set_translation(mesh, x=0, y=0, z=0):
    mesh.position = (x, y, z)

def set_translation_animated(mesh, x, y, z):
    t = 0
    delta = 0.01
    old_x = mesh.position[0]
    old_y = mesh.position[1]
    old_z = mesh.position[2]
    while(t<=1):
        current_x = ((x-old_x)*t + old_x)
        current_y = ((y-old_y)*t + old_y)
        current_z = ((z-old_z)*t + old_z)
        mesh.position = (current_x, current_y, current_z)
        t+=delta
        time.sleep(0.02)


def translate_animated(mesh, x, y, z):
    t = 0
    delta = 0.01
    old_x = mesh.position[0]
    old_y = mesh.position[1]
    old_z = mesh.position[2]
    while(t<=1):
        current_x = ((x)*t + old_x)
        current_y = ((y)*t + old_y)
        current_z = ((z)*t + old_z)
        mesh.position = (current_x, current_y, current_z)
        t+=delta
        time.sleep(0.02)

        












