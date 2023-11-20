class ObservableList:
    def __init__(self, initial_data=None):
        self._list = initial_data if initial_data else []
        self._observers = []

    def add_observer(self, observer):
        if callable(observer):
            self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, index=None, old_value=None, new_value=None):
        for observer in self._observers:
            if callable(observer):
                observer(index, old_value, new_value)

    def append(self, item):
        self._list.append(item)
        self.notify_observers(len(self._list) - 1, None, item)

    def extend(self, items):
        start_index = len(self._list)
        self._list.extend(items)
        for index, value in enumerate(items, start=start_index):
            self.notify_observers(index, None, value)

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, value):
        old_value = self._list[index]
        self._list[index] = value
        self.notify_observers(index, old_value, value)

    def __delitem__(self, index):
        deleted_item = self._list[index]
        del self._list[index]
        self.notify_observers(index, deleted_item, None)

    def __len__(self):
        return len(self._list)

    def __repr__(self):
        return repr(self._list)


if __name__ == "__main__":

    def on_list_change(index, old_value, new_value):
        print(f"Item update: {index} from {old_value} to {new_value}")

    observable_list = ObservableList([1, 2, 3])
    observable_list.add_observer(on_list_change)

    observable_list.append(4)
    observable_list.extend([5, 6])
    observable_list[0] = 10
    del observable_list[1]

    observable_list.append({"item": "test"})
    observable_list[-1]["item"] = "Another test"
