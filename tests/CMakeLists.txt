configure_file(spe3/SPE3CASE1.DATA spe3/SPE3CASE1.DATA COPYONLY)

foreach(prog parse state props schedule wells)
    add_python_test(${prog} ${prog}.py)
endforeach()
