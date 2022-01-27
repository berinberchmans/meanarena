    def drawMeanies(self):
        self.meanie = []
        # First, for every entry in mLoc, create an object to be drawn in
        # "meanie"
        for i in range(len(self.gameWorld.mLoc)):
            self.addMeanieToDrawList(self.gameWorld.mLoc[i])

        # Then draw the objects in "meanie" on the display pane
        for i in range(len(self.gameWorld.mLoc)): 
            self.drawMeanie(i)

    # Add picture objects to the list of things to draw
    def addMeanieToDrawList(self, location):
        if config.useImage:
            self.meanie.append(Image(self.convert2(location.x, location.y), "images/meanie.png"))
        else:
            self.meanie.append(Circle(self.convert2(location.x, location.y),  self.cSize*self.magnify).setFill('blue'))
            #self.meanie[i].setFill('blue')

    # Draw the object at location "index" in the list "meanie"
    def drawMeanie(self, index):
        self.meanie[index].draw(self.pane)

    # Function used by the gameWorld to add a new Meanie to the
    # display.
    #
    # This is the only access function, since otherwise the display
    # accesses information from the gameWorld (rather than the other
    # way around).
    #def addMeanieToDisplay(self, location):
    #    self.addMeanieToDrawList(location)
    #    # This is always the last element in the list
    #    drawMeanie(len(self.meanie))
