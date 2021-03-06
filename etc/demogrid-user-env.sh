# -------------------------------------------------------------------------- #
# Copyright 2010, University of Chicago                                      #
#                                                                            #
# Licensed under the Apache License, Version 2.0 (the "License"); you may    #
# not use this file except in compliance with the License. You may obtain    #
# a copy of the License at                                                   #
#                                                                            #
# http://www.apache.org/licenses/LICENSE-2.0                                 #
#                                                                            #
# Unless required by applicable law or agreed to in writing, software        #
# distributed under the License is distributed on an "AS IS" BASIS,          #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
# See the License for the specific language governing permissions and        #
# limitations under the License.                                             #
# -------------------------------------------------------------------------- #


if [ -z "${DEMOGRID_LOCATION}" ]; then
    echo "Environment variable DEMOGRID_LOCATION is not set"  1>&2
    return 1
fi

PATH="${DEMOGRID_LOCATION}/bin:${PATH}";

if [ -z "${PYTHONPATH}" ]; then
    PYTHONPATH="${DEMOGRID_LOCATION}/lib"
fi
PYTHONPATH="${DEMOGRID_LOCATION}/lib:${PYTHONPATH}"

