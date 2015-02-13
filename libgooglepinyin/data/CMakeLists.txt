include(TestBigEndian)

test_big_endian(BIGENDIAN)
if (BIGENDIAN)
    set(DATA_SUFFIX ".be")
else (BIGENDIAN)
    set(DATA_SUFFIX "")
endif (BIGENDIAN)

add_custom_command(OUTPUT dict_pinyin.dat
                   DEPENDS dictbuilder
                   COMMAND dictbuilder ${CMAKE_CURRENT_SOURCE_DIR}/rawdict_utf16_65105_freq${DATA_SUFFIX}.txt ${CMAKE_CURRENT_SOURCE_DIR}/valid_utf16${DATA_SUFFIX}.txt)

add_custom_target(datafile ALL DEPENDS dict_pinyin.dat)

configure_file(googlepinyin.pc.in ${CMAKE_CURRENT_BINARY_DIR}/googlepinyin.pc)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dict_pinyin.dat DESTINATION ${libdir}/googlepinyin/data)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/googlepinyin.pc DESTINATION ${libdir}/pkgconfig)
