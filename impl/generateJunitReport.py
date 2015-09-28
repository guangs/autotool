import sys
import re
import shutil
import os

def read_result_file(result_file):
    content = ''
    with open(result_file,'r') as f:
        content = f.read()
    return content

def get_racetrack_url(result_content):
    racetrack_url_pattern = r'http://racetrack[-dev]*\.eng\.vmware\.com/result\.php\?id=\d+'
    m = re.search(racetrack_url_pattern,result_content)
    if m:
        return m.group()
    else:
        return None

def get_cases(result_content):
    case_pattern = r'<TR>\n\s\s<TD>(.*)</TD>\n\s\s<TD>(.*)</TD>\n\s\s<TD>(.*)</TD>\n\s\s<TD bgcolor=.*>(.*)</TD>\n\s</TR>'
    m = re.findall(case_pattern,result_content)
    if m:
        return m
    else:
        return None

def get_table(result_content):
    table_pattern = r'<TABLE[\s\S]*</TABLE>'
    m = re.search(table_pattern,result_content)
    if m:
        return re.sub(r'\n', '',m.group())
    else:
        return None

def generate_properties_for_racetrack_report(result_content):
    with open('racetrack.properties','w') as f:
        f.write('Table=%s\n' % get_table(result_content))
        f.write('RacetrackURL=%s\n' % get_racetrack_url(result_content))

class JunitReporter(object):

    report = []

    def __init__(self,cases):
        self.cases = cases

    def add_pass_case(self,case_name,suite_name):
        self.report.append('    <testcase name="%s" classname="%s" time="0.0"/>\n' % (case_name,suite_name))

    def add_failure_case(self,case_name,suite_name,fail_reason=' '):
        case_item = '''    <testcase name="%s" classname="%s" time="0.0">
      <failure>%s</failure>
    </testcase>
''' % (case_name,suite_name,fail_reason)
        self.report.append(case_item)

    def generate_junit_report(self):
        print 'starting to generate Junit report...'
        self.report.append('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.report.append('<testsuites>\n')
        suites = set([ re.sub(r'[&<>]*','',case[0]) for case in self.cases])
        for suite_name in suites:
            self.report.append('  <testsuite name="%s" time="0.0">\n' % suite_name)
            for case in self.cases:
                case_description = re.sub(r'[&<>]*','',case[1])
                case_name = re.sub(r'[&<>]*','',case[2])
                case_result = re.sub(r'[&<>]*','',case[3])
                if case_result.upper() == 'PASS':
                    self.add_pass_case(case_name + '->'+ case_description,suite_name)
                else:
                    self.add_failure_case(case_name + '->'+ case_description,suite_name,fail_reason=case_result)
            self.report.append('  </testsuite>\n')
        self.report.append('</testsuites>')
        report = ''.join(self.report)
        with open('report.xml','w') as f:
            f.write(report)
        print 'Junit report is finished'

def main():
    result_file = sys.argv[1]  # Linux\conf\result.txt file generated by automation script
    raw_result = read_result_file(result_file)
    cases = get_cases(raw_result)
    jr = JunitReporter(cases)
    jr.generate_junit_report()
    generate_properties_for_racetrack_report(raw_result)
if __name__ == '__main__':
    main()