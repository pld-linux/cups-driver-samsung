# TODO
# - name of spec and package?
Summary:	CLP-510 Linux Driver
Summary(pl):	Linuksowy sterownik do CLP-510
Name:		cups-driver-samsung
Version:	1.1.4
Release:	0.8
License:	?
Group:		Applications
Source0:	http://downloadcenter.samsung.com/content/DR/200503/20050322102424156_lpp-%{version}-19-i386.tar.gz
# Source0-md5:	16b04c89a94378b4c8571c593f1ddcd3
Source1:	http://downloadcenter.samsung.com/content/DR/200503/20050322102424156_lpp-%{version}-19-ppc.tar.gz
# Source1-md5:	d64b336d692718013099c5d72ffa7600
URL:		http://www.samsung.com/Products/PrinterandMultifunction/ColorLaserPrinters/CLP_510XAA.asp
BuildRequires:	cups-devel
Requires:	cups
Requires:	cups-clients
Obsoletes:	cups-driver-clp-510
ExclusiveArch:	%{ix86} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_datadir	%(cups-config --datadir 2>/dev/null)
%define 	_libdir		%(cups-config --serverbin 2>/dev/null)
%define		_cupsppddir	%{_datadir}/model
%define 	_cupsfilterdir	%{_libdir}/filter
%define 	_cupsfontsdir	%{_datadir}/fonts

%description
Linux driver for Samsung CLP-510 color laser printer which features
speeds of up to 6 ppm color, 25 ppm black and has built-in duplexing.

%description -l pl
Linuksowy sterownik do kolorowych drukarek laserowych Samsung CLP-510
osi±gaj±cych szybko¶æ do 6 stron/minutê w kolorze lub 25 stron/minutê
w czerni, z wbudowanym dupleksem.

%prep
%ifarch %{ix86}
%setup -qcT -a0
%endif
%ifarch ppc
%setup -qcT -a1
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd image
install -d $RPM_BUILD_ROOT{%{_cupsppddir},%{_cupsfilterdir},%{_cupsfontsdir},%{_sysconfdir}}

#cp -a bin/Linux/x86/filters/* $RPM_BUILD_ROOT%{_cupsfilterdir}
# duplicate with cups
#rm -f $RPM_BUILD_ROOT%{_cupsfilterdir}/hpgltops
#rm -f $RPM_BUILD_ROOT%{_cupsfilterdir}/imagetops
#rm -f $RPM_BUILD_ROOT%{_cupsfilterdir}/pstops
#rm -f $RPM_BUILD_ROOT%{_cupsfilterdir}/texttops
# afaik PLD cups already has support for those
#rm -f $RPM_BUILD_ROOT%{_cupsfilterdir}/*print

# only these two needed?
# http://www.linuxprinting.org/show_printer.cgi?recnum=Samsung-CLP-500
cp -a bin/Linux/x86/filters/{ppmtosplc,pscms} $RPM_BUILD_ROOT%{_cupsfilterdir}

# perhaps the fonts should be from elsewhere? cups?
cp -a data/fonts/{`cat <<EOF | xargs | tr ' ' ','
AvantGarde-Book
AvantGarde-BookOblique
AvantGarde-Demi
AvantGarde-DemiOblique
Bookman-Demi
Bookman-DemiItalic
Bookman-Light
Bookman-LightItalic
Charter-Bold
Charter-BoldItalic
Charter-Italic
Charter-Roman
Helvetica
Helvetica-Bold
Helvetica-BoldOblique
Helvetica-Narrow
Helvetica-Narrow-Bold
Helvetica-Narrow-BoldOblique
Helvetica-Narrow-Oblique
Helvetica-Oblique
NewCenturySchlbk-Bold
NewCenturySchlbk-BoldItalic
NewCenturySchlbk-Italic
NewCenturySchlbk-Roman
Palatino-Bold
Palatino-BoldItalic
Palatino-Italic
Palatino-Roman
Times-Bold
Times-BoldItalic
Times-Italic
Times-Roman
Utopia-Bold
Utopia-BoldItalic
Utopia-Italic
Utopia-Regular
ZapfChancery-MediumItalic
ZapfDingbats
EOF
`} $RPM_BUILD_ROOT%{_cupsfontsdir}

cp -a ppd/C/*.ppd $RPM_BUILD_ROOT%{_cupsppddir}

# a config what ./bin/Linux/x86/cfggen generates
cat > $RPM_BUILD_ROOT%{_sysconfdir}/linuxprint.cfg <<'EOF'
<?xml version="1.0"?>
<linux root="/" system="cups">
	<option name="ghostscript" value="/usr/bin/gs"/>
	<option name="address" value="localhost"/>
	<option name="port" value="631"/>
	<option name="lpr" value="/usr/bin/lp"/>
<!--
	<printer ppd="/usr/share/cups/model/CLP-510splc.ppd" queue="CLP-510">
		<option name="Resolution" value="600"/>
		<option name="Duplex" value="None"/>
		<option name="PageSize" value="A4"/>
		<option name="InputSlot" value="AUTO"/>
		<option name="MediaType" value="Normal"/>
		<option name="JCLJamrecovery" value="RWJOff"/>
	</printer>
-->
</linux>
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/linuxprint.cfg
%attr(755,root,root) %{_cupsfilterdir}/*
%{_cupsppddir}/*
%{_cupsfontsdir}/*
