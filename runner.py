import pyreally
import logging
import time
import pprint

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    try:
        pp = pprint.PrettyPrinter(depth=6)
        really = pyreally.Really()
        really.login_anonymous()
        # f = really.get("/users/5983404145292480512/")
        # print("I got a future: %s" % f)
        # print("The result is: %s" % f.result())

        query = "firstName = $name"
        query_args = {"name": "Ahmed"}
        f2 = really.query("/users")
        print("The QUERY result:")
        result = f2.result()
        print(result)
        pp.pprint(map(lambda obj: obj.body, result.items))
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

        # f3 = really.create(pyreally.R("/users"), {"firstName": "Ahmed", "age": 55})
        # print("The QUERY result: %s" % f3.result())
        # res = f3.result()
        # pp.pprint(res.get_raw_response())

        # f4 = really.delete(res.r)
        # print("DELETE result: %s" % f4.result())

    except KeyboardInterrupt:
        print("KEYBOARD INTERRUPT, Closing REALLY")
        really.close()
    except pyreally.OperationError as e:
        print("OPERATION FAILED %s" % e)
        time.sleep(10)
        really.close()