#!/usr/bin/env python

#
# Generated  by generateDS.py.
# Python 3.5.2 (default, Nov 17 2016, 17:05:23)  [GCC 5.4.0 20160609]
#
# Command line options:
#   ('-f', '')
#   ('--no-dates', '')
#   ('--no-versions', '')
#   ('--super', 'sros2keystore.utils.dds.xml.permissions')
#   ('-o', 'sros2keystore/sros2keystore/utils/dds/xml/permissions.py')
#   ('-s', 'sros2keystore/sros2keystore/utils/dds/xml/permissions_sub.py')
#
# Command line arguments:
#   sros2keystore/sros2keystore/resources/dds/xml/permissions.xsd
#
# Command line:
#   /usr/local/bin/generateDS -f --no-dates --no-versions --super="sros2keystore.utils.dds.xml.permissions" -o "sros2keystore/sros2keystore/utils/dds/xml/permissions.py" -s "sros2keystore/sros2keystore/utils/dds/xml/permissions_sub.py" sros2keystore/sros2keystore/resources/dds/xml/permissions.xsd
#
# Current working directory (os.getcwd()):
#   xml
#

import sys
from lxml import etree as etree_

import sros2keystore.utils.dds.xml.permissions as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'utf-8'

#
# Data representation classes
#


class PermissionsNodeSub(supermod.PermissionsNode):
    def __init__(self, permissions=None):
        super(PermissionsNodeSub, self).__init__(permissions, )
supermod.PermissionsNode.subclass = PermissionsNodeSub
# end class PermissionsNodeSub


class PermissionsSub(supermod.Permissions):
    def __init__(self, grant=None):
        super(PermissionsSub, self).__init__(grant, )
supermod.Permissions.subclass = PermissionsSub
# end class PermissionsSub


class GrantSub(supermod.Grant):
    def __init__(self, name=None, subject_name=None, validity=None, allow_rule=None, deny_rule=None, default=None):
        super(GrantSub, self).__init__(name, subject_name, validity, allow_rule, deny_rule, default, )
supermod.Grant.subclass = GrantSub
# end class GrantSub


class ValiditySub(supermod.Validity):
    def __init__(self, not_before=None, not_after=None):
        super(ValiditySub, self).__init__(not_before, not_after, )
supermod.Validity.subclass = ValiditySub
# end class ValiditySub


class RuleSub(supermod.Rule):
    def __init__(self, domains=None, publish=None, subscribe=None, relay=None):
        super(RuleSub, self).__init__(domains, publish, subscribe, relay, )
supermod.Rule.subclass = RuleSub
# end class RuleSub


class DomainIdSetSub(supermod.DomainIdSet):
    def __init__(self, id=None, id_range=None):
        super(DomainIdSetSub, self).__init__(id, id_range, )
supermod.DomainIdSet.subclass = DomainIdSetSub
# end class DomainIdSetSub


class DomainIdRangeSub(supermod.DomainIdRange):
    def __init__(self, min=None, max=None):
        super(DomainIdRangeSub, self).__init__(min, max, )
supermod.DomainIdRange.subclass = DomainIdRangeSub
# end class DomainIdRangeSub


class CriteriaSub(supermod.Criteria):
    def __init__(self, topics=None, partitions=None, data_tags=None):
        super(CriteriaSub, self).__init__(topics, partitions, data_tags, )
supermod.Criteria.subclass = CriteriaSub
# end class CriteriaSub


class TopicExpressionListSub(supermod.TopicExpressionList):
    def __init__(self, topic=None):
        super(TopicExpressionListSub, self).__init__(topic, )
supermod.TopicExpressionList.subclass = TopicExpressionListSub
# end class TopicExpressionListSub


class PartitionExpressionListSub(supermod.PartitionExpressionList):
    def __init__(self, partition=None):
        super(PartitionExpressionListSub, self).__init__(partition, )
supermod.PartitionExpressionList.subclass = PartitionExpressionListSub
# end class PartitionExpressionListSub


class DataTagsSub(supermod.DataTags):
    def __init__(self, tag=None):
        super(DataTagsSub, self).__init__(tag, )
supermod.DataTags.subclass = DataTagsSub
# end class DataTagsSub


class TagNameValuePairSub(supermod.TagNameValuePair):
    def __init__(self, name=None, value=None):
        super(TagNameValuePairSub, self).__init__(name, value, )
supermod.TagNameValuePair.subclass = TagNameValuePairSub
# end class TagNameValuePairSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PermissionsNode'
        rootClass = supermod.PermissionsNode
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PermissionsNode'
        rootClass = supermod.PermissionsNode
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    from StringIO import StringIO
    parser = None
    doc = parsexml_(StringIO(inString), parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PermissionsNode'
        rootClass = supermod.PermissionsNode
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PermissionsNode'
        rootClass = supermod.PermissionsNode
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('#from sros2keystore.utils.dds.xml.permissions import *\n\n')
        sys.stdout.write('import sros2keystore.utils.dds.xml.permissions as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
