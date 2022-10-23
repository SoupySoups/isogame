import logging
import utils.logs as logs
import math
import time


class AnimationManager:
    @logs.logBeforeAndAfter(
        before="Setting up animation manager...",
        after="Animation manager successfully set up.",
        level=logging.DEBUG,
    )
    def __init__(self, yuckie) -> None:
        self.ies = {}
        self.loadYuckie(yuckie)
        self.changedLayers = set()

    def animate(self, objs, dt) -> None:
        for obj in objs:
            diff = time.time() - obj.frStart
            modified = False
            length = self.getLength(obj.yuckieId)
            maxFr = self.maxFrame(obj.yuckieId)
            if diff >= length:
                obj.frStart = time.time()
                obj.frCnt = 0
                modified = True
            elif diff > length / (maxFr + 1) and obj.frCnt < maxFr:
                obj.frCnt += 1
                modified = True
            if obj.vel.length != 0:
                speed = 1
                obj.x -= (obj.vel.x * speed) * dt
                obj.y += (obj.vel.y * speed) * dt
                obj.z += (obj.vel.z * speed) * dt
                modified = True
            if modified:
                self.changedLayers.add(math.floor(obj.z))

    def loadYuckie(self, filename: str):
        with open(filename, "r") as f:
            for cnt, line in enumerate(f.readlines()):
                ns = line.replace(" ", "")
                if ns.startswith("#"):
                    continue
                sp = ns.split("(")[1:]
                if len(sp) != 4:
                    raise ValueError(f"Invalid line {cnt} in {filename}")
                self.ies[sp[0]] = {
                    "base": int(sp[1]),
                    "frames": list(map(int, sp[2].split(","))),
                    "length": float(sp[3]),
                }

    def getFrame(self, id, frame):
        ie = self.ies[id]
        all = [ie["base"]] + ie["frames"]
        return all[frame]

    def getLength(self, id):
        return self.ies[id]["length"]

    def maxFrame(self, id):
        return len(self.ies[id]["frames"])
