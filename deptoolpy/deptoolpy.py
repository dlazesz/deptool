#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os


def import_pyjnius(class_path):
    """
    PyJNIus can only be imported once per Python interpreter and one must set the classpath before importing...
    """
    # Check if autoclass is already imported...
    if 'autoclass' not in locals() and 'autoclass' not in globals():

        # Tested on Ubuntu 16.04 64bit with openjdk-8 JDK and JRE installed:
        # sudo apt install openjdk-8-jdk-headless openjdk-8-jre-headless

        # Set JAVA_HOME for this session
        try:
            os.environ['JAVA_HOME']
        except KeyError:
            os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'

        os.environ['CLASSPATH'] = ':'.join((class_path, os.environ.get('CLASSPATH', ''))).rstrip(':')

        # Set path and import jnius for this session
        from jnius import autoclass
    else:
        import sys
        from jnius import cast, autoclass  # Dummy autoclass import to silence the IDE
        class_loader = autoclass('java.lang.ClassLoader')
        cl = class_loader.getSystemClassLoader()
        ucl = cast('java.net.URLClassLoader', cl)
        urls = ucl.getURLs()
        cp = ':'.join(url.getFile() for url in urls)

        print('Warning: PyJNIus is already imported with the following classpath: {0}'.format(cp), file=sys.stderr)

    # Return autoclass for later use...
    return autoclass


class DepToolPy:
    class_path = os.path.join(os.path.dirname(__file__), 'depTool')

    def __init__(self):
        # All classes should be imported in __init__()
        autoclass = import_pyjnius(DepToolPy.class_path)
        self._jstr = autoclass('java.lang.String')
        self._dt = autoclass('hu.nytud.gate.util.DepTool')
        self.target_fields = ['pos', 'fature']

    def process_sentence(self, sen, field_names):
        for tok in sen:
            lemma_tag = tok[field_names[1]] + tok[field_names[2]]
            string = tok[field_names[0]]
            tok.append(self._dt.getPos(self._jstr(lemma_tag.encode('UTF-8')), self._jstr(string.encode('UTF-8'))))
            tok.append(self._dt.getFeatures(self._jstr(lemma_tag.encode('UTF-8')), self._jstr(string.encode('UTF-8'))))
        return sen

    @staticmethod
    def prepare_fields(field_names):
        return [field_names['string'], field_names['lemma'], field_names['hfstana']]


if __name__ == '__main__':
    deptool = DepToolPy()
    sent = [['Az', '[{"ana": "az[/Det|Art.Def]=az", "feats": "[/Det|Art.Def]", "lemma": "az", "readable_ana": "az[/Det|Art.Def]"}, {"ana": "az[/Det|Pro]=az+[Nom]=", "feats": "[/Det|Pro][Nom]", "lemma": "az", "readable_ana": "az[/Det|Pro] + [Nom]"}, {"ana": "az[/N|Pro]=az+[Nom]=", "feats": "[/N|Pro][Nom]", "lemma": "az", "readable_ana": "az[/N|Pro] + [Nom]"}]', 'az', '[/Det|Art.Def]'],
            ['árvíztűrőtükörúrógép', '[]', 'árvíztűrőtükörúrógép', '[/Adv]'],
            ['hasznos', '[{"ana": "hasznos[/Adj]=hasznos+[Nom]=", "feats": "[/Adj][Nom]", "lemma": "hasznos", "readable_ana": "hasznos[/Adj] + [Nom]"}, {"ana": "haszon[/N]=haszn+os[_Adjz:s/Adj]=os+[Nom]=", "feats": "[/Adj][Nom]", "lemma": "hasznos", "readable_ana": "haszon[/N]=haszn + os[_Adjz:s/Adj] + [Nom]"}, {"ana": "haszon[/N]=haszn+os[_Nz:s/N]=os+[Nom]=", "feats": "[/N][Nom]", "lemma": "hasznos", "readable_ana": "haszon[/N]=haszn + os[_Nz:s/N] + [Nom]"}]', 'hasznos', '[/N][Nom]'],
            ['.', '[{"ana": "", "feats": "[Punct]", "lemma": ".", "readable_ana": ""}]', '.', '[Punct]']]
    print('\n'.join(str(e) for e in deptool.process_sentence(sent, [0, 2, 3])))
