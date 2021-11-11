"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 1/7/21

"""
actions = ["execute,doNothing",
           "setFileAttribute, doNothing",
           "addToRegistryRunKeys,doNothing",
           "setFileAttribute,doNothing",
           "HTTP,doNothing",
           "execute, runInHE",
           "HTTP, redirectToDecoy/honeyTraffic/corrouptTraffic/blockTraffic",
           "HTTP, doNothing",
           "tasklist, doNothing",
           "queryRegistry, doNothing",
           "dir, doNothing",
           "dir, delayedResponse",
           "addToRegistryRunKeys, doNothing",
           "compress, doNothing",
           "copy, doNothing",
           "dir/tasklist/queryRegistry,doNothing",
           "copy, deleteData",
           "queryRegistry/dir/tasklist, doNothing",
           "dir, redirectToHoneyDir",
           "compress, honeyCompress",
           "copy, delayedResponse",
           "queryRegistry,honeyRegistry",
           "tasklist, honeySwList",
           "copy,doNothing"]

if __name__ == '__main__':
    attach_action = set()
    deception_action = set()

    for action in actions:
        aa, da = action.split(',')

        if '/' in aa:
            for v in aa.split('/'):
                attach_action.add(v.strip())
        else:
            attach_action.add(aa.strip())

        if '/' in da:
            for v in da.split('/'):
                deception_action.add(v.strip())
        else:
            deception_action.add(da.strip())

    for i in attach_action:
        print(i)
    # print(attach_action)
    # print(deception_action)
    print("********************************************************************************")
    for i in deception_action:
        print(i)
