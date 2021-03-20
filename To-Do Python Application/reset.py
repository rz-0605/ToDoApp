# Run this to reset file
import pickle
events = {}
oufile = open("ToDoEvents", 'wb')
pickle.dump(events, oufile)
oufile.close()

