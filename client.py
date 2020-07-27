##import os
##os.environ["PYRO_LOGFILE"] = "pyro.log"
##os.environ["PYRO_LOGLEVEL"] = "DEBUG"
##
import Pyro4
import Pyro4.util
import Pyro4.futures
import sys

if __name__=='__main__':
    #Pyro4.config.COMMTIMEOUT=10
    try:
        front_end = Pyro4.Proxy("PYRONAME:fe")
        print(front_end.callMe())
    except Exception:
        print("".join(Pyro4.util.getPyroTraceback()))
        print ("error")
        exit()
    done=False
    rm=None
    while True:
        front_end._pyroReconnect()
        if done==False:
            try:
                 rm=front_end.connectRM()
            except:
                  print("Sorry.....Server down")
                  sys.exit()
        done=True
        print("What are you going to do?")
        request=input("press: \n q for query \n u for update \n c for quit \ninput:").strip()
        if request=="q":
            title=input("What's the name of the movie? ").strip()
            response="no"
            #print(done)
            try:
                front_end._pyroReconnect()
                response=front_end.queryRating(title.lower(),rm)
            except Exception:
                print("Pyro traceback:")
                print("".join(Pyro4.util.getPyroTraceback()))
                print("Sorry.....Server down")
                sys.exit()
            if response=="no":
                print("Unsuccessful")
            else:
                print(response)
            #do something
        elif request=="u":
            title=input("What's the name of the movie? ").strip()
            number=int(input("What's ur rating? ").strip())
            front_end._pyroReconnect()
            try:
                response=front_end.sendUpdate(number,title.lower(),rm)
            except Exception:
                print("".join(Pyro4.util.getPyroTraceback()))

                print("Sorry.....Server down")
                sys.exit()
            print(response)
            if response=="no":
                print("Update Unsuccessful")
            else:
                print("Success")

        elif request=="c":
            print("exiting....")
            front_end._pyroReconnect()
            front_end.disconnect(rm)
            #print(response)
            #print(front_end.incrementCounter())
            sys.exit()
        else:
            print("##############################\n Invalid Input \n ###########################")
            continue
        cont=input("Do you want to continue? \n Y (or any keys) or N\n input:").strip().lower()
        print (cont)
        if cont=="n":
            print("exiting....")
            front_end.disconnect(rm)
            front_end._pyroRelease()
            break
        else:
            continue
        

    print("exiting...")
    sys.exit()
    


