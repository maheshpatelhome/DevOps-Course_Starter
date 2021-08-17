class ToDoViewModel:
    def __init__(self, items, recent_date, user_is_writer = False):
        self._items = items
        self.recent_date = recent_date 
        self._user_is_writer = user_is_writer

    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        todo_items=[]
        for item in self._items:
            if item.status.upper() == "TO DO":
                todo_items.append(item)
        return todo_items

    @property
    def doing_items(self):
        doing_items=[]
        for item in self._items:
            if item.status.upper() == "DOING":
                doing_items.append(item)
        return doing_items

    @property
    def done_items(self):
        self.determine_done_items()
        return self._done_items
        
    @property 
    def recent_done_items(self):
        self.determine_done_items()
        self._recent_items=[]
        done_items = self._done_items
        for item in done_items:
            if (item.last_modified > self.recent_date):
                self._recent_items.append(item)
        return self._recent_items

    @property
    def older_done_items(self):
        self.determine_done_items()
        self._older_items=[]
        done_items = self._done_items
        for item in done_items:
            if (item.last_modified <= self.recent_date):
                self._older_items.append(item)
        return self._older_items
    
    @property
    def user_is_writer(self):
        return self._user_is_writer


    def determine_done_items(self):
        self._done_items=[]
        for item in self._items:
            if item.status.upper() == "DONE":
                self._done_items.append(item)
