from Menu import Menu


class Menu_Screen_Mission(Menu):

    def select(self):
        return self._callbacls[self.current_index]()
