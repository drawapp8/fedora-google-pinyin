function buildOne() {
	name=$1
	mkdir -p build/$name; 
	cd build/$name; 
	cmake ../../$name -DCMAKE_INSTALL_PREFIX=/usr;
	make;make install;
	cd -
}

buildOne "ibus-googlepinyin"
buildOne "libgooglepinyin"

