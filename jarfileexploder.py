import zipfile
import json

def read_zipfile(zip_file, extname='.java'):
    """
    Generates files or folders inside a zipfile
    :param zip_file: zipfile to be search
    :param extname: file with extension filename to be searched
    :return: generates files or folders inside the zip file
    """
    with zipfile.ZipFile(zip_file) as lines:
        for line in lines.infolist():
            if line.filename.endswith(extname):
                yield line.filename

def search_zipfile(zip_file, extname, search):
    """
    This is a lesser code implementation of read_zipfile_openfile before
    :param zip_file: zipfile to be searched
    :param extname: file with extension filename to be searched
    :param search:  keyword to be looking for in a file
    :return: a tuple java file as key and a dictionary of where search keyword found and line number as key
    """
    with zipfile.ZipFile(zip_file) as unzipped:
        for line in unzipped.infolist():
            if line.filename.endswith(extname):
                with unzipped.open(line.filename, 'r') as myfile:
                    flines = myfile.readlines()
                    lines = {i+1 : j.strip().decode("utf-8") for i, j in enumerate(flines) if search in j}
                    if lines:
                        yield {line.filename: lines}

def to_json(zip_file, extname, search):
    """ generates a json equivalent of the result """
    return json.dumps([i for i in search_zipfile(zip_file, extname, search)])

def write_to_file(jarfile, file='results.txt', mode='a', extname='.java', search=b'version'):
    with open(file, mode) as f:
        for i in search_zipfile(jarfile, extname=extname, search=search):
            for k, v in i.items():
                f.write(k + '\n')
                for z in v:
                    for a, b in z.items():
                        f.write(a)
                        f.write('\t' + b + '\n')

def decompile(decompiler='cfr_0_122.jar', zip_file='', dump='./tmp'):
    """
    Decompile all jar files
    :param decompiler: decompiler to use default to cfr_0_122
    :param jarfile: jar file to be decompile
    :param dump: folder to dump sources
    :return: none
    """
    from subprocess import call
    call(['java', '-jar', decompiler, zip_file, '--caseinsensitivefs', 'true', '--outputdir', dump])


if __name__ == '__main__':
    JARFILE = 'sample.jar'
    EXTNAME = '.java'
    #sample
    print(to_json(JARFILE, EXTNAME, b'version'))

