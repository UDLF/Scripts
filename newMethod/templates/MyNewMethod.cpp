/* <MyNewMethod.cpp>
 *
 * MyNewMethod implementation file
 *
 ***********************************************************************************
 *
 * This file is part of Unsupervised Distance Learning Framework (UDLF).
 *
 * UDLF is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * UDLF is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with UDLF.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include <iostream>

#include "MyNewMethod.hpp"

/* Constructor */
MyNewMethod::MyNewMethod() {

}

void MyNewMethod::loadParameters() {
    Exec exec = Exec::getInstance();

    //MyNewMethod Parameters (read from the configuration file)
}

void MyNewMethod::checkParameters() {
    /*
    if (l > n) {
        std::cout << "L can't be greater than N" << std::endl;
        std::cout << "Aborting..." << std::endl;
        exit(1);
    }
    */
}

void MyNewMethod::initDataStructuresUdl() {
    std::cout << "Initializing data structures..." << std::endl;

    //rkLists.resize(n*l);
    //initMatrix(matrix);

    std::cout << "Initialized successfully!" << std::endl;
}

void MyNewMethod::initDataStructuresFusion() {
    std::cerr << "WARNING: The Fusion Mode is not implemented for this method! Aborting ...\n";
    exit(1);
}

void MyNewMethod::prepareInput() {
    if (inputFileFormat == "MATRIX") {
        if (inputMatrixType == "DIST") {
            genRksFromDistMatrix();
        } else { //SIM
            genRksFromSimMatrix();
        }
    }
}

void MyNewMethod::prepareOutput() {
    if (outputFileFormat == "MATRIX") {
        if (outputMatrixType == "DIST") {
            genDistMatrixFromRks();
        } else { //SIM
            genSimMatrixFromRks();
        }
    }
}

void MyNewMethod::runUdlMethod() {
    std::cout << "\n Executing MyNewMethod!\n\n";
}

void MyNewMethod::runFusionMethod() {
    std::cerr << "WARNING: The Fusion Mode is not implemented for this method! Aborting ...\n";
    exit(1);
}
