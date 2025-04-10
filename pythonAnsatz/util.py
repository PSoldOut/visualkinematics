import numpy as np
import pythreejs as three
from pythreejs import *
from pythreejs import SpriteMaterial, Sprite
import time
from scipy.spatial.transform import Rotation as R, Slerp







#die angles werden in der Reihenfolge zurückgegeben wie order es vorgibt bsp: order="ZXY" rückgabe->[z,x,y]
def quaternion_to_euler(x, y, z, w, order="ZYZ"):
    quaternion = [x, y, z, w]
    euler_angles = R.from_quat(quaternion).as_euler(order, degrees=True)
    return euler_angles


#die angles müssen in der Reihenfolge angegeben werden wie es in der order steht bsp: angles=[y,x,z] order="YXZ"
def euler_to_rot_mat(angles, order="ZYZ"):
    r = R.from_euler(order, angles, degrees=True)
    return r.as_matrix()

#die angles werden in der Reihenfolge zurückgegeben wie order es vorgibt bsp: order="ZXY" rückgabe->[z,x,y]
def rot_matrix_to_euler(rot_mat, order="ZYZ"):
    r = R.from_matrix(rot_mat)
    return r.as_euler(order, degrees=True)

def rot_matrix_to_quaternion(rot_mat):
    r = R.from_matrix(rot_mat).as_quat()
    return r

#die angles müssen in der Reihenfolge angegeben werden wie es in der order steht bsp: angles=[y,x,z] order="YXZ"
def euler_to_quaternion(angles, order='ZYZ'):
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




def order_angles(x, y, z, order):
    if order == "ZYZ" or order == "zyz":
        return [z,y,z]
    elif order == "XYX" or order == "xyx":
        return [x,y,x]
    elif order == "XZX" or order == "xzx":
        return [x,z,x]
    elif order == "YXY" or order == "yxy":
        return [y,x,y]
    elif order == "YZY" or order == "yzy":
        return [y,z,y]
    elif order == "ZXZ" or order == "zxz":
        return [z,x,z]
    elif order == "XYZ" or order == "xyz":
        return [x,y,z]
    elif order == "XZY" or order == "xzy":
        return [x,z,y] 
    elif order == "YZX" or order == "yzx":
        return [y,z,x]
    elif order == "YXZ" or order == "yxz":
        return [y,x,z]
    elif order == "ZXY" or order == "zxy":
        return [z,x,y]
    elif order == "ZYX" or order == "zyx":
        return [z,y,x]




def quaternion_multiply(q1, q2):
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2
    
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    
    return [x, y, z, w]








def create_axes(len, font_scale=0.4, show_labels=True, name=""):
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


    font_offset=0.3

    ttx = TextTexture("X", color='#000000')
    x_label = Sprite(
    material=SpriteMaterial(map=ttx, transparent=True, opacity=0.9, depthWrite=False),
    position=[len+font_offset, 0, 0],
    scale=(font_scale, font_scale, font_scale),
    visible=show_labels
    )

    tty = TextTexture("Y", color='#000000')
    y_label = Sprite(
    material=SpriteMaterial(map=tty, transparent=True, opacity=0.9, depthWrite=False),
    position=[0, len+font_offset, 0],
    scale=(font_scale, font_scale, font_scale),
    visible=show_labels
    )

    ttz = TextTexture("Z", color='#000000')
    z_label = Sprite(
    material=SpriteMaterial(map=ttz, transparent=True, opacity=0.9, depthWrite=False),
    position=[0, 0, len+font_offset],
    scale=(font_scale, font_scale, font_scale),
    visible=show_labels
    )

    axes_group.add([x_label, y_label, z_label])


    cyl_x = create_cylinder([len,0,0], radiusTop=0.1, radiusBottom=0.01, height=0.3, color=[255,0,0])
    rotate(cyl_x, [0,0,90], "XYZ")
    axes_group.add(cyl_x)

    cyl_y = create_cylinder([0,len,0], radiusTop=0.1, radiusBottom=0.01, height=0.3, color=[0,255,0])
    rotate(cyl_y, [180,0,0], "XYZ")
    axes_group.add(cyl_y)

    cyl_z = create_cylinder([0,0,len], radiusTop=0.1, radiusBottom=0.01, height=0.3, color=[0,0,255])
    rotate(cyl_z, [-90,0,0], "XYZ")
    axes_group.add(cyl_z)

    if name!="":
        n = TextTexture(name, color='#000000')
        name_label = Sprite(
        material=SpriteMaterial(map=n, transparent=True, opacity=1, depthWrite=False),
        position=[font_offset, font_offset, font_offset],
        scale=(font_scale, font_scale, font_scale),
        visible=show_labels
        )
        axes_group.add([name_label])

    return axes_group







def create_grid_XY(size, density):
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



def create_grid_XZ(size, density):
    line_material = three.LineBasicMaterial(color='#777777')
    line_material.transparent = True
    line_material.opacity = 0.5

    grid_group = three.Group()
    for i in range((int)((-size/2)*(1/density)), (int)((size/2)*(1/density))+1):
        points1 = [[-size/2,0,i*density],[size/2,0,i*density]]
        points2 = [[i*density,0,-size/2],[i*density,0,size/2]]
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






def createQuad(pos, width, height, depth, color=[0,255,0], transparent=True):
    # Erstelle die Geometrie (Breite, Höhe, Tiefe)
    geometry = three.BoxGeometry(width=width, height=height, depth=depth)
    # Material (Farbe & Eigenschaften)
    hex_color = f'#{color[0]:02X}{color[1]:02X}{color[2]:02X}'
    material = three.MeshStandardMaterial(color=hex_color, metalness=0.5, roughness=0.8, transparent=transparent, opacity=0.5)
    # Erstelle das Mesh (Geometrie + Material)
    mesh = three.Mesh(geometry, material)
    mesh.position = (pos[0], pos[1], pos[2])
    return mesh




def create_cylinder(pos, radiusTop=1, radiusBottom=1, height=2, radialSegments=32, color=[255,0,0], transparent=True):
    # Erstelle eine CylinderGeometry
    geometry = CylinderGeometry(
    radiusTop=radiusTop,     # Radius oben
    radiusBottom=radiusBottom,  # Radius unten
    height=height,        # Höhe
    radialSegments=radialSegments  # Auflösung rundherum
    )
    hex_color = f'#{color[0]:02X}{color[1]:02X}{color[2]:02X}'
    material = three.MeshStandardMaterial(color=hex_color, metalness=0.5, roughness=0.8, transparent=transparent, opacity=0.5)

    # Mesh aus Geometrie + Material
    cylinder = Mesh(
        geometry=geometry,
        material=material,
        position=pos
    )
    return cylinder



def apply_rot_matrix_animated(mesh, rot_mat, speed=100):
    q = R.from_matrix(rot_mat).as_quat() 
    old_quat = mesh.quaternion
    new_quat = quaternion_multiply(mesh.quaternion, (q[0], q[1], q[2], q[3]))
    t = 0
    delta = 0.002
    while(t <= 1):
        n = slerp_quaternion(old_quat, new_quat, t)
        mesh.quaternion = [n[0], n[1], n[2], n[3]]
        t += delta
        time.sleep(1/speed)
    n = slerp_quaternion(old_quat, new_quat, 1)
    mesh.quaternion = [n[0], n[1], n[2], n[3]]




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









def set_scale(mesh, scale):
    mesh.scale = scale
    

def set_scale_animated(mesh, scale):
    old_x = mesh.scale[0]
    old_y = mesh.scale[1]
    old_z = mesh.scale[2]
    t = 0
    delta = 0.02
    while(t<=1):
        current_x = (scale[0]-old_x)*t + old_x
        current_y = (scale[0]-old_y)*t + old_y
        current_z = (scale[0]-old_z)*t + old_z
        mesh.scale = (current_x, current_y, current_z)
        t+=delta
        time.sleep(0.01)


#die angles müssen in der Reihenfolge angegeben werden wie es in der order steht bsp: angles=[y,x,z] order="YXZ"
def rotate_animated(mesh, angles, order="ZYZ"):
    q_final = quaternion_multiply(mesh.quaternion, euler_to_quaternion(angles, order))
    time.sleep(0.5)
    delta = 0.5
    if angles[0] < 0:
        delta *= -1
    counter = delta
    while counter <= abs(angles[0]):
        q = euler_to_quaternion([delta, 0, 0], order)
        mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
        counter+=abs(delta)
        time.sleep(0.01)
    time.sleep(0.5)
    delta = 0.5
    if angles[1] < 0:
        delta *= -1
    counter = delta
    while counter <= abs(angles[1]):
        q = euler_to_quaternion([0, delta, 0], order)
        mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
        counter+=abs(delta)
        time.sleep(0.01)
    time.sleep(0.5)
    delta = 0.5
    if angles[2] < 0:
        delta *= -1
    counter = delta
    while counter <= abs(angles[2]):
        q = euler_to_quaternion([0, 0, delta], order)
        mesh.quaternion = quaternion_multiply(mesh.quaternion, q)
        counter+=abs(delta)
        time.sleep(0.01)
    mesh.quaternion = q_final
    time.sleep(0.5)
    



#die angles müssen in der Reihenfolge angegeben werden wie es in der order steht bsp: angles=[y,x,z] order="YXZ"
def rotate_global_animated(mesh, angles, order="ZYZ"):
    time.sleep(0.5)
    delta = 0.5
    if angles[0] < 0:
        delta *= -1
    counter = delta
    while counter < abs(angles[0]):
        q = euler_to_quaternion([delta, 0, 0], order)
        mesh.quaternion = quaternion_multiply(q, mesh.quaternion)
        counter+=abs(delta)
        time.sleep(0.01)
    time.sleep(0.5)
    delta = 0.5
    if angles[1] < 0:
        delta *= -1
    counter = delta
    while counter < abs(angles[1]):
        q = euler_to_quaternion([0, delta, 0], order)
        mesh.quaternion = quaternion_multiply(q, mesh.quaternion)
        counter+=abs(delta)
        time.sleep(0.01)
    time.sleep(0.5)
    delta = 0.5
    if angles[2] < 0:
        delta *= -1
    counter = delta
    while counter < abs(angles[2]):
        q = euler_to_quaternion([0, 0, delta], order)
        mesh.quaternion = quaternion_multiply(q, mesh.quaternion)
        counter+=abs(delta)
        time.sleep(0.01)
    time.sleep(0.5)



def move(robot, x_vel, theta_vel):
    rot_mat_z = np.array([
    [np.cos(theta_vel), -np.sin(theta_vel), 0],
    [np.sin(theta_vel),  np.cos(theta_vel), 0],
    [0,             0,             1]
    ])

    apply_rot_matrix(robot, rot_mat_z)
    x = robot.quaternion[0]
    y = robot.quaternion[1]
    z = robot.quaternion[2]
    w = robot.quaternion[3]
    translate(robot, [np.cos(np.radians(quaternion_to_euler(x,y,z,w,"XYZ")[2]))*x_vel, np.sin(np.radians(quaternion_to_euler(x,y,z,w,"XYZ")[2]))*x_vel, 0])



def rotate_global(mesh, angles, order="ZYZ"):
    mesh.quaternion = quaternion_multiply(euler_to_quaternion(angles, order[::-1]), mesh.quaternion)

def rotate(mesh, angles, order="ZYZ"):
    q = euler_to_quaternion(angles, order)
    mesh.quaternion = quaternion_multiply(mesh.quaternion, q)

def set_rotation(mesh, angles, order="ZYZ"):
    q = euler_to_quaternion(angles, order=order)
    mesh.quaternion = [q[0], q[1], q[2], q[3]]

def set_rotation_global(mesh, angles, order="ZYZ"):
    set_rotation(mesh, angles[::-1], order[::-1])

def translate(mesh, vec):
    mesh.position = (mesh.position[0]+vec[0], mesh.position[1]+vec[1], mesh.position[2]+vec[2])

def set_translation(mesh, vec):
    mesh.position = vec

def set_translation_animated(mesh, vec, speed=50.0):
    t = 0
    delta = 0.01
    old_x = mesh.position[0]
    old_y = mesh.position[1]
    old_z = mesh.position[2]
    while(t<=1):
        current_x = ((vec[0]-old_x)*t + old_x)
        current_y = ((vec[1]-old_y)*t + old_y)
        current_z = ((vec[2]-old_z)*t + old_z)
        mesh.position = (current_x, current_y, current_z)
        t+=delta
        time.sleep(1.0/speed)
    current_x = ((vec[0]-old_x)*1 + old_x)
    current_y = ((vec[1]-old_y)*1 + old_y)
    current_z = ((vec[2]-old_z)*1 + old_z)
    mesh.position = (current_x, current_y, current_z)
    time.sleep(1.0/speed)



def translate_animated(mesh, vec, speed=50.0):
    t = 0
    delta = 0.01
    old_x = mesh.position[0]
    old_y = mesh.position[1]
    old_z = mesh.position[2]
    while(t<=1):
        current_x = ((vec[0])*t + old_x)
        current_y = ((vec[1])*t + old_y)
        current_z = ((vec[2])*t + old_z)
        mesh.position = (current_x, current_y, current_z)
        t+=delta
        time.sleep(1.0/speed)
    current_x = ((vec[0])*1 + old_x)
    current_y = ((vec[1])*1 + old_y)
    current_z = ((vec[2])*1 + old_z)
    mesh.position = (current_x, current_y, current_z)
    time.sleep(1.0/speed)
        












