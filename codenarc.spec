Name:          codenarc
Version:       0.24.1
Release:       7
Summary:       A static analysis tool for Groovy source code
License:       ASL 2.0
Url:           http://codenarc.github.io/CodeNarc/
Source0:       https://github.com/CodeNarc/CodeNarc/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: maven-local mvn(junit:junit) mvn(log4j:log4j:1.2.17) mvn(org.apache.ant:ant)
BuildRequires: mvn(org.codehaus.gmavenplus:gmavenplus-plugin) mvn(org.codehaus.groovy:groovy)
BuildRequires: mvn(org.codehaus.groovy:groovy-ant) mvn(org.codehaus.groovy:groovy-xml) mvn(org.gmetrics:GMetrics)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)

BuildArch:     noarch

%description
CodeNarc analyzes Groovy code for defects,bad practices,inconsistencies,style issues and more.
A flexible framework for rules,rulesets and custom rules means it is easy to configure CodeNarc to fit into your project.
Build tool,framework support and report generation are all enterprise ready.

%package       help
Summary:       Help documents for codenarc
Provides:      %{name}-javadoc = %{version}-%{release}
Obsoletes:     %{name}-javadoc < %{version}-%{release}

%description   help
Help documents for codenarc.

%prep
%autosetup -n CodeNarc-%{version}

find . -name '*.jar' -exec rm -f {} ';'
find . -name '*.class' -exec rm -f {} ';'
rm -rf docs/*

cp -p site-pom.xml pom.xml

install -d src/main/java/org/codenarc/analyzer
cp -p src/main/groovy/org/codenarc/analyzer/SuppressionAnalyzer.java \
 src/main/java/org/codenarc/analyzer/

%pom_xpath_inject pom:project/pom:properties '
  <antVersion>1.9.6</antVersion>
  <gmetricsVersion>0.7</gmetricsVersion>
  <junitVersion>4.12</junitVersion>
  <log4jVersion>1.2.17</log4jVersion>
  <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>'

%pom_xpath_set pom:properties/pom:targetJdk 1.6
%pom_xpath_set pom:properties/pom:groovyVersion 2.4.5

%pom_add_plugin org.apache.maven.plugins:maven-compiler-plugin:3.5.1 . "
<configuration>
    <source>\${targetJdk}</source>
    <target>\${targetJdk}</target>
</configuration>"

%pom_add_plugin org.codehaus.gmavenplus:gmavenplus-plugin:1.5 . "
 <executions>
  <execution>
   <goals>
    <goal>generateStubs</goal>
    <goal>testGenerateStubs</goal>
   </goals>
  </execution>
 </executions>"

%pom_add_dep org.apache.ant:ant:'${antVersion}' . "<optional>true</optional>"
%pom_add_dep org.codehaus.groovy:groovy:'${groovyVersion}'
%pom_add_dep org.codehaus.groovy:groovy-ant:'${groovyVersion}'
%pom_add_dep org.codehaus.groovy:groovy-xml:'${groovyVersion}'
%pom_add_dep org.gmetrics:GMetrics:'${gmetricsVersion}'
%pom_add_dep junit:junit:'${junitVersion}'
%pom_add_dep log4j:log4j:'${log4jVersion}'

%mvn_file org.%{name}:CodeNarc %{name} CodeNarc

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc CHANGELOG.txt README.md
%license LICENSE.txt NOTICE.txt

%files help -f .mfiles-javadoc

%changelog
* Mon Feb 14 2022 wangkai <wangkai385@huawei.com> - 0.24.1-7
- Rebuild for fix log4j1.x cves

* Thu Mar 5 2020 tangjing <tangjing30@huawei.com> - 0.24.1-6
- Package init
