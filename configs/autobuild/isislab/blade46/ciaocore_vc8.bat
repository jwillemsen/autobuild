rem $Id$
rem perl C:\ACE\autobuild\autobuild.pl ciaocore_vc8.xml

cd C:\ACE\autobuild
set CVS_RSH=plink
cvs -q -d :ext:isisbuilds@cvs.doc.wustl.edu:/project/cvs-repository -z9 up -P -d


perl autobuild.pl configs\autobuild\isislab\blade46\ciaocore_vc8.xml
