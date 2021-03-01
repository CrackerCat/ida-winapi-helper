import requests, idaapi, os, idc, json

TARGET = 'D:\\winapi.json'
funcDB = {}

def InitFn():
    global TARGET, funcDB
    if len(funcDB): return
    if os.path.exists(TARGET):
        funcDB = json.load(open(TARGET))
        return
    print "Creating DB ..."
    def cache(prefix):
        headers = requests.get('%stoc.json' % prefix).json()
        for hdr in headers['items'][0]['children'][1]['children']:
            title = hdr['toc_title'].decode()
            # print title
            data = requests.get('%s%s/toc.json' % (prefix, hdr['href'].decode())).json()
            if data['items'] and data['items'][0] and 'children' in data['items'][0].keys():
                for child in data['items'][0]['children']:
                    try:
                        tag = child['toc_title'].decode()
                        if 'function' in tag:
                            href = child['href'].decode()
                            fn = tag.split()[0]
                            # print "Func: ", fn
                            funcDB[fn] = 'https://docs.microsoft.com/en-us/' + href
                    except Exception as e:
                        import traceback
                        print(child)
                        traceback.print_exc()
                        return
    cache("https://docs.microsoft.com/en-us/windows/win32/api/")
    cache("https://docs.microsoft.com/en-us/windows-hardware/drivers/ddi/")
    with open(TARGET, "w") as fp:
        fp.write(json.dumps(funcDB))
    print("Done!")

def Fuck():
    InitFn()
    name, _ = idaapi.get_highlight(idaapi.get_current_viewer())
    if name in funcDB.keys():
        os.startfile(funcDB[name], 'open')

idaapi.CompileLine('static xFuck() { RunPythonStatement("Fuck()"); }')
AddHotkey("Ctrl+,", "xFuck")
