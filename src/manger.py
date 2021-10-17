from sgengine.lifecycle import Node, EventLoop


class Manager(Node):
    def start(self) -> None:
        self.loop = EventLoop.get_instance()

        self.childs.append(self.loop)
        return super().start()