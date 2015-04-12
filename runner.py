import pyreally
import logging
import time
import pprint
import random
logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    try:
        pp = pprint.PrettyPrinter(depth=6)
        really = pyreally.Really()
        really.login_anonymous()
        res1 = really.create(pyreally.R("/users"), {"firstName": "Kareem", "lastName": "Sameer", "age": 55})
        print(res1.result())
        time.sleep(2)
        f = really.get(res1.result().r)
        print("The result is: %s" % f.result().get_raw_response())

        print("QUERY BEFORE DELETE")
        ff = really.query("/users", "_r = $r", {"r": str(res1.result().r)}, include_total=True)
        print(ff.result().get_raw_response())

        f3 = really.delete(f.result().r)
        print(" I got : %s" % f3.result().get_raw_response())
        time.sleep(2)
        # f = really.get(res1.result().r)
        # print("I got a result: %s" % f.result().get_raw_response())
        print("QUERY AFTER DELETE")
        ff = really.query("/users", "_r = $r", {"r": str(f.result().r)}, include_total=True)
        print(ff.result().get_raw_response())
        # query = "firstName = $name"
        # query_args = {"name": "Ahmed"}
        # f2 = really.query("/users")
        # print("The QUERY result:")
        # result = f2.result()
        # print(result)
        # pp.pprint(map(lambda obj: obj.body, result.items))
        # nextToken = result.next_token
        # print("NEXT TOKEN: %s" % nextToken)
        # f2 = really.query("/users", limit=2, include_total=True, pagination_token=nextToken)
        # print("The QUERY result:")
        # pp.pprint(f2.result().items)
        # print("Total: %s" % f2.result().count)
        #

        # result = f2.result()
        # pp.pprint(result.get_raw_response())
        # nextToken = result.next_token
        # print("NEXT TOKEN: %s" % nextToken)
        # f2 = really.query("/users", limit=2, include_total=True, pagination_token=nextToken)
        # print("The QUERY result:")
        # pp.pprint(f2.result().items)


        # f4 = really.delete(res.r)
        # print("DELETE result: %s" % f4.result())
        # names = ["Ahmed", "khaled", "ibrahim", "hussein", "zaki", "Ismail", "Sinar", "Refaey", "Amal" , "Ihab"]
        # results = []
        # for i in range(500):
        #     results.append(really.create(pyreally.R("/users"), {"firstName": random.choice(names), "lastName": random.choice(names), "age": 55}))
        #
        # for result in results:
        #     print("The QUERY result: %s" % result.result())
        #     currentHatem = result.result()
        #     pp.pprint(currentHatem.body['fullName'])

        # sub_result = really.subscribe(currentHatem.r, None, currentHatem.rev, ['firstName'])
        # print("I got %s" % sub_result.result().get_raw_response())
        # # hatem = really.get('/users/5967264813380931584/')
        #
        # ops = [pyreally.Update('set', 'lastName', 'Medhat')]
        # resp = really.update(currentHatem.r, ops, currentHatem.rev)
        # print(resp.result().get_raw_response())
        # hatem2 = really.get(currentHatem.r)
        # print("Hatem is now %s:" % hatem2.result().body)
        #
        #
        # ops = [pyreally.Update('set', 'firstName', 'Mika')]
        # logging.info("Hatem now is: %s" % currentHatem.body)
        # resp = really.update(currentHatem.r, ops, hatem2.result().rev)
        # print(resp.result().get_raw_response())
        # hatem2 = really.get(currentHatem.r)
        # print("Hatem is now %s:" % hatem2.result().body)

        time.sleep(5)
    except KeyboardInterrupt:
        print("KEYBOARD INTERRUPT, Closing REALLY")
        really.close()
    except pyreally.OperationError as e:
        print("OPERATION FAILED %s" % e)
        time.sleep(10)
        really.close()