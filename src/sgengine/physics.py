from typing import Tuple
import sgengine
from sgengine import lifecycle


def is_colliding(node: lifecycle.Node, check_self=False) -> Tuple[bool, lifecycle.Node]:
    if node.solid and node.rect != None:
        for other in sgengine.event_loop().alive_nodes():
            if other.id != node.id or check_self:
                if other.solid and other.rect != None and node.rect.colliderect(other.rect):
                    return True, other

    return False, None

class Gravity(lifecycle.Node):

    def start(self) -> None:
        self.global_gravity_settings = GravitySettings(enabled=False, gravity_velocity=5)
        return super().start()

    def update(self) -> None:
        nodes = sgengine.event_loop().alive_nodes()

        for node in nodes:
            if not issubclass(type(node), Gravity):
                self.apply_gravity(node)
        return super().update()

    def apply_gravity(self, node: lifecycle.Node) -> bool:
        if node.rect != None and node.gravity_settings.enabled:
            last_pos = node.rect.copy()
            node.rect.move_ip(0, node.gravity_settings.gravity_velocity if node.gravity_settings.gravity_velocity != None else self.global_gravity_settings.gravity_velocity)
            colliding, other = is_colliding(node)
            if colliding:
                node.rect.topleft = last_pos.topleft
            return True

        return False


class GravitySettings:
    def __init__(self, enabled = False, gravity_velocity: float = None) -> None:
        self.enabled = enabled
        self.gravity_velocity = gravity_velocity
        pass

