from numpyPablo import custom_add_vectors, custom_vector_mag, custom_dot_product, custom_subtract_vectors, custom_vector_normalize, custom_vector_s_m, custom_cross_product
from math import pi, atan2, acos



class Intercept(object):
	def __init__(self, distance, point, normal, obj, texcoords):
		self.distance = distance
		self.point = point
		self.normal = normal
		self.obj = obj
		self.texcoords = texcoords



class Shape(object):

	def __init__(self, position, material):
		self.position = position
		self.material = material

	def ray_intersect(self, origin, direction):

		return None


class Sphere(Shape):

	def __init__(self, position, radius, material):
		self.radius = radius
		super().__init__(position, material)


	def ray_intersect(self, origin, direction):

		L = custom_subtract_vectors(self.position, origin)
		lengthL = custom_vector_mag(L)
		tca = custom_dot_product(L, direction)
		d = (lengthL**2 - tca **2) ** 0.5

		if d > self.radius:
			return None

		thc = (self.radius ** 2 - d ** 2) ** 0.5

		t0 = tca - thc
		t1 = tca + thc

		if t0 < 0:
			t0 = t1

		if t0 < 0:
			return None
		
		D = custom_vector_s_m(t0,direction)
		P = custom_add_vectors(origin, D)
		point_normal = custom_subtract_vectors(P, self.position)
		point_normal = custom_vector_normalize(point_normal)

		u = atan2(point_normal[2], point_normal[0]) / (2 * pi) + 0.5
		v = acos(point_normal[1]) / pi

		return Intercept(distance = t0,
						 point = P,
						 normal = point_normal,
						 obj = self,
						 texcoords = (u,v))


class Plane(Shape):

	def __init__(self, position, normal, material):
		self.normal = normal
		super().__init__(position, material)


	def ray_intersect(self, origin, direction):

		denom = custom_dot_product(direction, self.normal)

		if abs(denom) <= 0.0001:
			return None

		num = custom_dot_product(custom_subtract_vectors(self.position, origin), self.normal)
		
		t = num / denom

		if t < 0:
			return None

		D = custom_vector_s_m(t,direction)
		P = custom_add_vectors(origin, D)

		return Intercept(distance = t,
						 point = P,
						 normal = self.normal,
						 obj = self,
						 texcoords = None)


class Disk(Plane):

	def __init__(self, position, normal, radius, material):
		self.radius = radius
		super().__init__(position, normal, material)


	def ray_intersect(self, origin, direction):
		planeIntersect = super().ray_intersect(origin, direction)
		
		if planeIntersect is None:
			return None

		contactDistance = custom_subtract_vectors(planeIntersect.point, self.position)
		contactDistance = custom_vector_mag(contactDistance)

		if contactDistance > self.radius:
			return None

		return Intercept(distance = planeIntersect.distance,
						 point = planeIntersect.point,
						 normal = self.normal,
						 obj = self,
						 texcoords = None)


class AABB(Shape):

	def __init__(self, position, size, material):
		super().__init__(position, material)

		self.planes = []
		self.size = size

		leftPlane =    Plane(custom_add_vectors(self.position, (-size[0] / 2,0,0)), (-1,0,0), material)
		rightPlane =   Plane(custom_add_vectors(self.position, ( size[0] / 2,0,0)), ( 1,0,0), material)
					  
		bottomPlane =  Plane(custom_add_vectors(self.position, (0,-size[1] / 2,0)), (0,-1,0), material)
		topPlane = 	   Plane(custom_add_vectors(self.position, (0, size[1] / 2,0)), (0, 1,0), material)
					   
		backPlane =    Plane(custom_add_vectors(self.position, (0,0,-size[2] / 2)), (0,0,-1), material)
		frontPlane =   Plane(custom_add_vectors(self.position, (0,0, size[2] / 2)), (0,0, 1), material)

		self.planes.append(leftPlane)
		self.planes.append(rightPlane)
		self.planes.append(bottomPlane)
		self.planes.append(topPlane)
		self.planes.append(backPlane)
		self.planes.append(frontPlane)

		self.boundsMin = [0,0,0]
		self.boundsMax = [0,0,0]

		self.bias = 0.001

		for i in range(3):
			self.boundsMin[i] = self.position[i] - (self.bias + size[i]/2)
			self.boundsMax[i] = self.position[i] + (self.bias + size[i]/2)
		

	def ray_intersect(self, origin, direction):
		intersect = None
		t = float('inf')

		u = 0
		v = 0

		for plane in self.planes:
			planeIntersect = plane.ray_intersect(origin, direction)

			if planeIntersect is not None:
				
				planePoint = planeIntersect.point

				if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
					if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
						if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
							if planeIntersect.distance < t:
								t = planeIntersect.distance
								intersect = planeIntersect

								if abs(plane.normal[0] > 0):
									u = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + self.bias * 2)
									v = 1 - (planePoint[1] - self.boundsMin[1]) / (self.size[1] + self.bias * 2)
								
								elif abs(plane.normal[1] > 0):
									u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + self.bias * 2) 
									v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + self.bias * 2) 

								elif abs(plane.normal[2] > 0):
									u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + self.bias * 2)
									v = 1 - (planePoint[1] - self.boundsMin[1]) / (self.size[1] + self.bias * 2)

		if intersect is None:
			return None

		return Intercept(distance = t,
						 point = intersect.point,
						 normal = intersect.normal,
						 obj = self,
						 texcoords = (u, v))




class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height

        self.top_plane = Plane(np.custom_add_vectors(self.position, (0, height / 2, 0)), (0, 1, 0), material)
        self.bottom_plane = Plane(np.custom_add_vectors(self.position, (0, -height / 2, 0)), (0, -1, 0), material)

    def ray_intersect(self, orig, dir):
        top_plane_intersect = self.top_plane.ray_intersect(orig, dir)
        bottom_plane_intersect = self.bottom_plane.ray_intersect(orig, dir)


        side_intercept = None

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
                    t0 = t1  

                y0 = orig[1] + t0 * dir[1]

                if y0 < self.position[1] - self.height / 2 or y0 > self.position[1] + self.height / 2:
                    t0 = None

                if t0 is not None:
                    side_intercept = Intercept(distance=t0,
                                               point=np.custom_add_vectors(orig, np.custom_multiply_vector_by_scalar(dir, t0)),
                                               normal=None, texcoords=None, obj=self)

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





class Triangle(Shape):

	def __init__(self, v0, v1, v2, material):
		self.v0 = v0
		self.v1 = v1
		self.v2 = v2

		self.v0v1 = custom_subtract_vectors(self.v1, self.v0)
		self.v0v2 = custom_subtract_vectors(self.v2, self.v0)

		self.normal = custom_vector_normalize(custom_cross_product(self.v0v1, self.v0v2))

		super().__init__(v0, material)


	def ray_intersect(self, origin, direction):
		pvec = custom_cross_product(direction, self.v0v2)
		det = custom_dot_product(self.v0v1, pvec)
		kEpsilon = 0.001	

		if abs(det) < kEpsilon:
			return None
		
		
		invDet = 1.0 / det 

		tvec = custom_subtract_vectors(origin, self.v0) 
		
		u = custom_dot_product(tvec, pvec) * invDet

		if u < 0 or u > 1:
			return None
	
		qvec = custom_cross_product(tvec, self.v0v1) 
		
		v = custom_dot_product(direction, qvec) * invDet

		if v < 0 or u + v > 1:
			return None

		t = custom_dot_product(self.v0v2,qvec) * invDet

		if t < 0:
			return None

		P = custom_add_vectors(origin, custom_vector_s_m(t, direction))

		return Intercept(distance=t,
							point=P,
							normal=self.normal,
							obj=self,
							texcoords=(u,v))



