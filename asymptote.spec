Name:		asymptote
Version:	2.04
Release:	%mkrel 1
Summary:	Descriptive vector graphics language for technical drawing
License:	LGPLv3+
Group:		Publishing
Url:		http://asymptote.sourceforge.net/
Source0:	http://downloads.sourceforge.net/asymptote/%{name}-%{version}.src.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libgc-devel >= 6.8
BuildRequires:	fftw3-devel
BuildRequires:	gsl-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	mesaglut-devel
BuildRequires:	zlib-devel
BuildRequires:	imagemagick
BuildRequires:	tetex-latex
BuildRequires:	texinfo
BuildRequires:	ghostscript

Requires:	python-imaging
Requires:	tkinter
Requires:	tetex-latex
Requires(post):	tetex
Requires(postun): tetex

%description
Asymptote is a powerful descriptive vector graphics language that 
provides a natural coordinate-based framework for technical drawing. 
Labels and equations are typeset with LaTeX, for high-quality 
PostScript output.

A major advantage of Asymptote over other graphics packages is that 
it is a programming language, as opposed to just a graphics program.

Features of Asymptote:

- provides a portable standard for typesetting mathematical figures, 
  just as TeX/LaTeX has become the standard for typesetting equations;

- generates and embeds 3D vector PRC graphics within PDF files;

- inspired by MetaPost, with a much cleaner, powerful C++-like 
  programming syntax and floating-point numerics;

- runs on all major platforms (UNIX, MacOS, Microsoft Windows);

- mathematically oriented (e.g. rotation of vectors by complex 
  multiplication);

- LaTeX typesetting of labels (for document consistency);

- uses simplex method and deferred drawing to solve overall size 
  constraint issues between fixed-sized objects (labels and 
  arrowheads) and objects that should scale with figure size;

- fully generalizes MetaPost path construction algorithms to three 
  dimensions;

- compiles commands into virtual machine code for speed without 
  sacrificing portability;

- high-level graphics commands are implemented in the Asymptote 
  language itself, allowing them to be easily tailored to specific 
  applications.

%prep
%setup -q

%build
%configure2_5x	--enable-gc=system \
		--with-latex=%{_datadir}/tex/latex \
		--with-context=%{_datadir}/tex/context
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Create symlinks for vim / emacs
install -d -m 755 %{buildroot}%{_datadir}/vim/syntax
ln -s ../../%{name}/asy.vim %{buildroot}%{_datadir}/vim/syntax/asy.vim

install -d -m 755 %{buildroot}%{_sysconfdir}/emacs/site-start.d
ln -s ../../../%{_datadir}/%{name}/asy-init.el %{buildroot}%{_sysconfdir}/emacs/site-start.d/asy-init.el
install -d -m 755 %{buildroot}%{_datadir}/emacs/site-lisp
ln -s ../../%{name}/asy-mode.el %{buildroot}%{_datadir}/emacs/site-lisp/asy-mode.el
ln -s ../../%{name}/asy-keywords.el %{buildroot}%{_datadir}/emacs/site-lisp/asy-keywords.el

# Move info file
mv %{buildroot}%{_infodir}/asymptote/asymptote.info %{buildroot}%{_infodir}/asymptote.info

# Icon
for size in 16x16 32x32 48x48
do
  install -d %{buildroot}%{_iconsdir}/hicolor/$size/apps
  convert -resize $size asy.ico %{buildroot}%{_iconsdir}/hicolor/$size/apps/asy.png
done

# Create xasy desktop file
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/xasy.desktop << EOF
[Desktop Entry]
Name=Asymptote
Comment=GUI tool for using Asymptote vector graphics 
Exec=%{_bindir}/xasy
Icon=asy
Terminal=false
StartupNotify=true
Type=Application
Categories=Graphics;VectorGraphics;
EOF

%clean
rm -rf %{buildroot}

%post
texhash
%_install_info %{name}.info
%_install_info asy-faq.info

%preun
texhash
%_remove_install_info %{name}.info
%_remove_install_info asy-faq.info

%files
%defattr(-,root,root,-)
%doc BUGS ChangeLog LICENSE* README ReleaseNotes TODO
%{_sysconfdir}/emacs/site-start.d/asy-init.el
%{_bindir}/asy
%{_bindir}/xasy
%{_datadir}/%{name}
%{_datadir}/applications/xasy.desktop
%{_datadir}/emacs/site-lisp/asy-mode.el
%{_datadir}/emacs/site-lisp/asy-keywords.el
%{_datadir}/vim/syntax/asy.vim
%{_datadir}/tex/latex/%{name}
%{_datadir}/tex/context/%{name}
%{_iconsdir}/hicolor/*/apps/asy.png
%{_infodir}/*.info*
%{_mandir}/man1/asy*
%{_mandir}/man1/xasy*
