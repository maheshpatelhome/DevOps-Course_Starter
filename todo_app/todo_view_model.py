class ToDoViewModel:
    def __init__(self, items, recent_date):
        self._items = items
        self.determine_done_items() 
        self.determine_recent_done_items(recent_date)
        self.determine_older_done_items(recent_date)
        self.determine_show_all_done()

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
        return self._done_items
        
    @property
    def show_all_done(self):
        return self._show_all_done
    
    @show_all_done.setter
    def show_all_done(self, value):
        self._show_all_done = value

    @property 
    def recent_done_items(self):
        return self._recent_items

    @property
    def older_done_items(self):
        return self._older_items

    def determine_show_all_done(self):
        done_items = self.done_items
        if len(done_items) >= 5:
            self._show_all_done = False
        else:
            self._show_all_done = True

    def determine_older_done_items(self, date_to_show_from):
        self._older_items=[]
        done_items = self._done_items
        for item in done_items:
            if (item.last_modified <= date_to_show_from):
                self._older_items.append(item)
    
    def determine_recent_done_items(self, date_to_show_from):
        self._recent_items=[]
        done_items = self._done_items
        for item in done_items:
            if (item.last_modified > date_to_show_from):
                self._recent_items.append(item)

    def determine_done_items(self):
        self._done_items=[]
        for item in self._items:
            if item.status.upper() == "DONE":
                self._done_items.append(item)