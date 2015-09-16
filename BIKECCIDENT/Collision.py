class Collision(object):
    def __init__(self,
                location,
                numCyclistsKilled,
                numCyclistsInjured,
                collisionId, collisionKey):
        self.location = location
        self.numCyclistsInjured = numCyclistsInjured
        self.numCyclistsKilled = numCyclistsKilled
        self.collisionId = collisionId
        self.collisionKey = collisionKey
        self.involvedVehicles = []
        self.contributingFactor = ''

    def add_involved_vehicle(self, involvedVehicle):
        self.involvedVehicles.append(involvedVehicle)
    
