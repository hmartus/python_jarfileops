import zipfile


def read_zipfile_extname(jarfile, extname='.class'):
    with zipfile.ZipFile(jarfile) as lines:
        for line in lines.infolist():
            if line.filename.endswith(extname):
                yield line.filename

def search_zipfile(zip_file, extname, search):
    """
    This is a lesser code implementation of read_zipfile_openfile before
    :param zip_file: zipfile to be searched
    :param extname: file with extension filename to be searched
    :param search:  keyword to be looking for in a file
    :return: a dictionary element with filename and a list of searched item was found
    """
    with zipfile.ZipFile(zip_file) as unzipped:
        for line in unzipped.infolist():
            if line.filename.endswith(extname):
                with unzipped.open(line.filename, 'r') as myfile:
                    flines = myfile.readlines()
                    lines = {i+1 : j.strip() for i,j in enumerate(flines) if search in j}
                    if lines:
                        yield {line.filename : lines}

def write_to_file(jarfile, file='results.txt', mode='a', extname='.java', search=b'version'):
    with open(file, mode) as f:
        for i in search_zipfile(jarfile, extname=extname, search=search):
            for k, v in i.items():
                f.write(k + '\n')
                for z in v:
                    for a, b in z.items():
                        f.write(a)
                        f.write('\t' + b + '\n')

def decompile(decompiler='cfr_0_122.jar', jarfile='oro-2.0.8.jar', dump='./tmp'):
    """
    Decompile all jar files
    :param decompiler: decompiler to use default to cfr_0_122
    :param jarfile: jar file to be decompile
    :param dump: folder to dump sources
    :return: none
    """
    from subprocess import call
    call(['java', '-jar', decompiler, jarfile, '--caseinsensitivefs', 'true', '--outputdir', dump])

def profile_me():
    write_to_file(jar_file2)

def display_dict(flist):
    for i, k in flist.items():
        print(i, str(k))

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped()

if __name__ == '__main__':
    jar_file2 = 'spring-webmvc-4.3.10.RELEASE-sources.jar'
    jar_samp = 'sample.jar'
    """
    import timeit
    t = timeit.Timer(setup='from __main__ import profile_me', stmt='profile_me()')
    print(t.timeit(1))
    
    write_to_file(jar_file2)
    decompile()
    """
    for i in search_zipfile(jar_file2, '.java', b'version'):
        print(i)