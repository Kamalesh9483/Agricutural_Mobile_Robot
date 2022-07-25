import multipartHTTPget
import imageDisplay

# importing the multiprocessing module
from multiprocessing import Process, Queue

if __name__ == '__main__':
    # Queue	
    rawImageQueue = Queue()
    outPutImageQueue  = Queue()
    
    # print("Hello world from main")
    # creating processes
    p1 = Process(target=multipartHTTPget.imageProcessor, args=(10, rawImageQueue, outPutImageQueue))
    p2 = Process(target=imageDisplay.imageDisplay, args=(10, rawImageQueue, outPutImageQueue))

    # print("Hello world from main")
    # starting process 1
    p1.start()
    # starting process 2
    p2.start()

    # wait until process 1 is finished
    p1.join()
    # wait until process 2 is finished
    p2.join()

    # both processes finished
    print("Done!")
