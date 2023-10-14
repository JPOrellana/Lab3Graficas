import numpyPablo as np
from math import pi, atan2, acos

class Intercept(object):
  def __init__(self,distance, point, normal,texcoords, obj):
    self.distance = distance
    self.point = point
    self.normal = normal
    self.texcoords = texcoords
    self.obj = obj

class Shape(object):
  def __init__(self, position, material):
    self.position = position
    self.material = material

  def ray_intersect(self, orig, dir):
    return None 
  

class Sphere(Shape):
  def __init__(self, position, radius, material):
    self.radius = radius
    super().__init__(position,material)
  
  def ray_intersect(self, orig, dir):
    L = np.custom_subtract_vector_from_vector(self.position, orig)
    lengthL = np.custom_linalg_norm(L)
    tca = np.custom_dot_product(L, dir)
    d = (lengthL**2 - tca**2)**0.5

    if d > self.radius:
      return None
    
    thc = (self.radius**2 - d**2)**0.5

    t0 = tca - thc
    t1 = tca + thc

    if t0 < 0:
      t0 = t1
    
    if t0 < 0:
      return None
    
    P = np.custom_add_vectors(orig, np.custom_multiply_vector_by_scalar(dir, t0))
    normal = np.custom_subtract_vector_from_vector(P,self.position)
    normal_norm = np.custom_linalg_norm(normal)
    if normal_norm != 0:
      normal = np.custom_multiply_vector_by_scalar(normal, 1 / normal_norm)

    u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
    v = acos(normal[1]) / pi
    return Intercept(distance = t0,
                     point = P,
                     normal = normal,
                     texcoords=(u,v),
                     obj = self)

class Plane(Shape):
  def __init__(self, position, normal, material):
    self.normal = np.custom_multiply_vector_by_scalar(normal, 1 / np.custom_linalg_norm(normal))

    super().__init__(position, material)

  def ray_intersect(self, orig, dir):
    denom = np.custom_dot_product(dir, self.normal)
    if abs(denom) <= 0.0001:
      return None
    num = np.custom_dot_product(np.custom_subtract_vector_from_vector(self.position,orig), self.normal)
    t = num / denom

    if t < 0:
      return None

    P = np.custom_add_vectors(orig, np.custom_multiply_vector_by_scalar(dir, t))

      
    return Intercept(distance = t,
                     point = P,
                     normal = self.normal,
                     texcoords= None,
                     obj = self)
  
class Disk(Plane):
  def __init__(self, position, normal,radius,material):
    self.radius = radius
    super().__init__(position , normal, material)

  def ray_intersect(self, orig, dir):
    planeInterect = super().ray_intersect(orig, dir)

    if planeInterect is None:
      return None
    
    contactDistance = np.custom_subtract_vector_from_vector(planeInterect.point, self.position) 
    contactDistance = np.custom_linalg_norm(contactDistance)

    if contactDistance > self.radius:
      return None
    
    return Intercept(distance = planeInterect.distance,
                     point = planeInterect.point,
                     normal = self.normal,
                     texcoords= None,
                     obj = self)
  
class AABB(Shape):

  def __init__(self, position, size, material):
    super().__init__(position, material)

    self.planes = []
    self.size = size

    
    leftPlane = Plane(np.custom_add_vectors(self.position , (-size[0]/ 2,0,0)), (-1,0,0), material )
    rightPlane = Plane(np.custom_add_vectors(self.position , (size[0] / 2,0,0)), (1,0,0), material )

    bottomPlane = Plane(np.custom_add_vectors(self.position, (0,-size[1] / 2,0)),(0,-1,0),material)
    topPlane = Plane(np.custom_add_vectors(self.position, (0,size[1] / 2,0)),(0,1,0),material)

    backPlane = Plane(np.custom_add_vectors(self.position, (0,0,-size[2] / 2)),(0,0,-1),material)
    frontPlane = Plane(np.custom_add_vectors(self.position, (0,0,size[2] / 2)),(0,0,1),material)

    self.planes.append(leftPlane)
    self.planes.append(rightPlane)
    self.planes.append(bottomPlane)
    self.planes.append(topPlane)
    self.planes.append(backPlane)
    self.planes.append(frontPlane)
    
    self.boundsMin = [0,0,0]
    self.boundsMax = [0,0,0]

    bias = 0.001

    for i in range(3):
      self.boundsMin[i] = self.position[i] - (bias + size[i]/2)
      self.boundsMax[i] = self.position[i] + (bias + size[i]/2)

  def ray_intersect(self, orig, dir):
    intersect = None
    t = float('inf')

    u = 0
    v = 0

    for plane in self.planes:

      planeIntersect = plane.ray_intersect(orig,dir)

      if planeIntersect is not None:

        planePoint = planeIntersect.point

        if self.boundsMin[0] < planePoint[0] < self.boundsMax[0]:
          if self.boundsMin[1] < planePoint[1] < self.boundsMax[1]:
            if self.boundsMin[2] < planePoint[2] < self.boundsMax[2]:
              if planeIntersect.distance < t:
                t = planeIntersect.distance
                intersect = planeIntersect

                if abs(plane.normal[0]) > 0:

                  u = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
                  v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                elif abs(plane.normal[1]) > 0:

                  u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                  v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                elif abs(plane.normal[2]) > 0:

                  u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                  v = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)

    if intersect is None:
      return None
    
    return Intercept(distance = t,
                     point = intersect.point,
                     normal = intersect.normal,
                     texcoords= (u,v),
                     obj = self)
  


    def ray_intersect(self, orig, dir):
        edge1 = np.custom_subtract_vector_from_vector(self.vertices[1], self.vertices[0])
        edge2 = np.custom_subtract_vector_from_vector(self.vertices[2], self.vertices[0])
        h = np.custom_cross_product(dir, edge2)
        a = np.custom_dot_product(edge1, h)

        if a > -0.00001 and a < 0.00001:
            return None

        f = 1.0 / a
        s = np.custom_subtract_vector_from_vector(orig, self.vertices[0])
        u = f * np.custom_dot_product(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = np.custom_cross_product(s, edge1)
        v = f * np.custom_dot_product(dir, q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * np.custom_dot_product(edge2, q)

        if t > 0.00001:
            intersect_point = np.custom_add_vectors(orig, np.custom_multiply_vector_by_scalar(dir, t))
            normal = np.custom_cross_product(edge1, edge2)
            normal_norm = np.custom_linalg_norm(normal)

            if normal_norm != 0:
                normal = np.custom_multiply_vector_by_scalar(normal, 1 / normal_norm)

            u, v = self.calculate_texcoords(u, v)

            return Intercept(distance=t,
                             point=intersect_point,
                             normal=normal,
                             texcoords=(u, v),
                             obj=self)
        else:
            return None

    def calculate_texcoords(self, u, v):
        return u, v




class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height

        # Define the top and bottom planes of the cylinder
        self.top_plane = Plane(np.custom_add_vectors(self.position, (0, height / 2, 0)), (0, 1, 0), material)
        self.bottom_plane = Plane(np.custom_add_vectors(self.position, (0, -height / 2, 0)), (0, -1, 0), material)

    def ray_intersect(self, orig, dir):
        # Check intersection with top and bottom planes
        top_plane_intersect = self.top_plane.ray_intersect(orig, dir)
        bottom_plane_intersect = self.bottom_plane.ray_intersect(orig, dir)

        # Check intersection with the side surface
        side_intercept = None

        # The side of the cylinder is bounded by two disks (top and bottom)
        # Calculate the side of the cylinder as a finite disk
        if top_plane_intersect is not None:
            side_intercept = top_plane_intersect
        elif bottom_plane_intersect is not None:
            side_intercept = bottom_plane_intersect
        else:
            a = dir[0] * dir[0] + dir[2] * dir[2]
            b = 2 * (dir[0] * (orig[0] - self.position[0]) + dir[2] * (orig[2] - self.position[2]))
            c = (orig[0] - self.position[0]) ** 2 + (orig[2] - self.position[2]) ** 2 - self.radius ** 2

            discriminant = b ** 2 - 4 * a * c

            if discriminant > 0:
                t0 = (-b - discriminant ** 0.5) / (2 * a)
                t1 = (-b + discriminant ** 0.5) / (2 * a)

                if t0 > t1:
                    t0, t1 = t1, t0

                if t0 < 0:
                    t0 = t1  # If t0 is negative, use t1

                y0 = orig[1] + t0 * dir[1]

                if y0 < self.position[1] - self.height / 2 or y0 > self.position[1] + self.height / 2:
                    t0 = None

                if t0 is not None:
                    side_intercept = Intercept(distance=t0,
                                               point=np.custom_add_vectors(orig, np.custom_multiply_vector_by_scalar(dir, t0)),
                                               normal=None, texcoords=None, obj=self)

        # Find the closest intersection
        closest_intercept = None

        if top_plane_intersect is not None:
            closest_intercept = top_plane_intersect

        if bottom_plane_intersect is not None:
            if closest_intercept is None or bottom_plane_intersect.distance < closest_intercept.distance:
                closest_intercept = bottom_plane_intersect

        if side_intercept is not None:
            if closest_intercept is None or side_intercept.distance < closest_intercept.distance:
                closest_intercept = side_intercept

        return closest_intercept







