#!/usr/bin/env python

#
# Generated  by generateDS.py.
# Python 3.5.2 (default, Nov 17 2016, 17:05:23)  [GCC 5.4.0 20160609]
#
# Command line options:
#   ('-f', '')
#   ('--no-dates', '')
#   ('--no-versions', '')
#   ('--super', 'sros2keystore.api.dds.xml.governance')
#   ('-o', 'sros2keystore/sros2keystore/api/dds/xml/governance.py')
#   ('-s', 'sros2keystore/sros2keystore/api/dds/xml/governance_sub.py')
#
# Command line arguments:
#   sros2keystore/sros2keystore/resources/dds/xml/governance.xsd
#
# Command line:
#   /usr/local/bin/generateDS -f --no-dates --no-versions --super="sros2keystore.api.dds.xml.governance" -o "sros2keystore/sros2keystore/api/dds/xml/governance.py" -s "sros2keystore/sros2keystore/api/dds/xml/governance_sub.py" sros2keystore/sros2keystore/resources/dds/xml/governance.xsd
#
# Current working directory (os.getcwd()):
#   xml
#

import sys
from lxml import etree as etree_

import sros2keystore.api.dds.xml.governance as supermod

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


class DomainAccessRulesNodeSub(supermod.DomainAccessRulesNode):
    def __init__(self, domain_access_rules=None):
        super(DomainAccessRulesNodeSub, self).__init__(domain_access_rules, )
supermod.DomainAccessRulesNode.subclass = DomainAccessRulesNodeSub
# end class DomainAccessRulesNodeSub


class DomainAccessRulesSub(supermod.DomainAccessRules):
    def __init__(self, domain_rule=None):
        super(DomainAccessRulesSub, self).__init__(domain_rule, )
supermod.DomainAccessRules.subclass = DomainAccessRulesSub
# end class DomainAccessRulesSub


class DomainRuleSub(supermod.DomainRule):
    def __init__(self, domains=None, allow_unauthenticated_participants=None, enable_join_access_control=None, discovery_protection_kind=None, liveliness_protection_kind=None, rtps_protection_kind=None, topic_access_rules=None):
        super(DomainRuleSub, self).__init__(domains, allow_unauthenticated_participants, enable_join_access_control, discovery_protection_kind, liveliness_protection_kind, rtps_protection_kind, topic_access_rules, )
supermod.DomainRule.subclass = DomainRuleSub
# end class DomainRuleSub


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


class TopicAccessRulesSub(supermod.TopicAccessRules):
    def __init__(self, topic_rule=None):
        super(TopicAccessRulesSub, self).__init__(topic_rule, )
supermod.TopicAccessRules.subclass = TopicAccessRulesSub
# end class TopicAccessRulesSub


class TopicRuleSub(supermod.TopicRule):
    def __init__(self, topic_expression=None, enable_discovery_protection=None, enable_liveliness_protection=None, enable_read_access_control=None, enable_write_access_control=None, metadata_protection_kind=None, data_protection_kind=None):
        super(TopicRuleSub, self).__init__(topic_expression, enable_discovery_protection, enable_liveliness_protection, enable_read_access_control, enable_write_access_control, metadata_protection_kind, data_protection_kind, )
supermod.TopicRule.subclass = TopicRuleSub
# end class TopicRuleSub


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
        rootTag = 'DomainAccessRulesNode'
        rootClass = supermod.DomainAccessRulesNode
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
        rootTag = 'DomainAccessRulesNode'
        rootClass = supermod.DomainAccessRulesNode
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
        rootTag = 'DomainAccessRulesNode'
        rootClass = supermod.DomainAccessRulesNode
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
        rootTag = 'DomainAccessRulesNode'
        rootClass = supermod.DomainAccessRulesNode
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('#from sros2keystore.api.dds.xml.governance import *\n\n')
        sys.stdout.write('import sros2keystore.api.dds.xml.governance as model_\n\n')
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
