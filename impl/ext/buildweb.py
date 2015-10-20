""" buildapi.eng.vmware.com """

import os
import requests
import urlparse
import re
import argparse
import pprint


BUILD_API_URL = 'http://buildapi.eng.vmware.com/'
OB_PATH = 'ob/'
SB_PATH = 'sb/'


def get_build_url_root(kind='official'):
    """ Return the root URL to build resources. """
    assert(kind in ['official', 'sandbox'])
    root_build_path = OB_PATH if kind == 'official' else SB_PATH
    uj = urlparse.urljoin
    return uj(uj(BUILD_API_URL, root_build_path), 'build/')


def get_build_urls(product, kind='official', **other_filters):
    """ Get a list of build URLs from buildapi. """
    assert(kind in ['official', 'sandbox'])
    build_url = get_build_url_root(kind)
    queries = {'product': product}
    # other_filters can include:
    # {
    #   'branch': branch_name,
    #   'buildtype': (release|beta|obj),
    # }
    if other_filters:
        queries.update(other_filters)
    if 'buildtype' in queries and queries['buildtype'] is None:
        queries.pop('buildtype')
    # default filters:
    default_filters = {
        'buildstate': 'succeeded',
        #'ondisk': 'True',
        '_order_by': '-id',
        '_limit': 16,
        '_format': 'json'}
    for fltr in default_filters:
        if fltr not in queries:
            queries[fltr] = default_filters[fltr]
    # GET
    print 'GET: %s?%s' % (build_url, '&'.join('%s=%s' % (n, v) for n, v in queries.items()))
    resp = requests.get(build_url, params=queries)
    return resp.json()['_list']


def make_deliverable(deliverable):
    """ Create a dictionary describing a deliverable. """
    mapping = {
        'id': 'id',
        'download_url': '_download_url',
        'path': 'path'
    }
    return {name:deliverable[mapping[name]] for name in mapping}


def get_build(build_url):
    """ Get infomation on a build, given its url. """
    deliverables = requests.get(urlparse.urljoin(
        BUILD_API_URL, build_url['_deliverables_url'])).json()['_list']
    return {
        'id': build_url['id'],
        'buildtype': build_url['buildtype'],
        'branch': build_url['branch'],
        'product': build_url['product'],
        'endtime': build_url['endtime'],
        'changeset': build_url['changeset'],
        'deliverables': [make_deliverable(dlitem) for dlitem in deliverables],
        'tree_url': build_url['_buildtree_url']
    }


def build_info_str(bld):
    """ Prints a build. """
    return '%10s  %12s  %12s  %10s  %10s  %s' % (
        bld['id'], bld['product'], bld['branch'], bld['buildtype'], bld['changeset'], bld['tree_url'])


def download_deliverable_file(product, target_pattern, local_dnld_dir,
                              branch=None, buildtype=None, buildid=None,kind='official'):
    """ Download the lastest version of a file. """
    kwargs = {}
    if branch:
        kwargs['branch'] = branch
    if buildtype:
        kwargs['buildtype'] = buildtype
    if buildid:
        kwargs['id'] = buildid
        
    #builds = get_build_urls(product, 'official', buildtype=buildtype, **kwargs)
    builds = get_build_urls(product, kind, **kwargs)
    
    latest = get_build(builds[0])
    print ">>> Downloading latest %s build: %d" % (product, latest['id'])
    # Find deliverable file
    target_path = None
    for dlvr in latest['deliverables']:
        matched = re.search(target_pattern, dlvr['path'])
        if matched:
            target_path = dlvr['path']
            break
    else:
        print "No deliverable file matches pattern '%s'" % target_pattern
        return None
    tree_url = latest['tree_url']
    download_url = os.path.join(tree_url, target_path)
    # Use the same name in buildweb
    local_file_path = os.path.join(local_dnld_dir, os.path.basename(target_path))
    with open(local_file_path, 'wb') as out:
        resp = requests.get(download_url, stream=True)
        for block in resp.iter_content(1024):
            out.write(block)
    print "        %s downloaded" % local_file_path
    return local_file_path


def main():
    """ main program. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--product',
                        required=True,
                        help='Product name in buildweb')
    parser.add_argument('-b', '--branch',
                        required=False,
                        help='Product branch')
    parser.add_argument('-t', '--buildtype',
                        choices=('release', 'beta', 'obj', 'opt'),
                        required=False,
                        help='Build type')
    parser.add_argument('-k', '--kind',
                        choices=('official', 'sandbox'),
                        required=False,
                        default='official',
                        help='Official or Sandbox build')
    parser.add_argument('-m', '--limit',
                        dest='_limit',
                        type=int,
                        required=False,
                        default=8,
                        help='Limit to N items')

    args = parser.parse_args()
    arg_vars = vars(args)
    #pprint.pprint(arg_vars)
    required = ['product']
    optionals = {name:arg_vars[name] for name in arg_vars if name not in required}
    builds = get_build_urls(args.product, **optionals)
    for build in builds:
        bld = get_build(build)
        print build_info_str(bld)


if __name__ == '__main__':
    main()
