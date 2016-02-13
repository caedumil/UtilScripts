#!/usr/bin/env  bash

#
# Based on scripts from
# https://gist.github.com/johntyree/3331662
#

LISTS=( "http://list.iblocklist.com/?list=ydxerpxkpcfqjaybcssw&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=gyisgnzbhppbvsphucsw&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=gihxqmhyunbxhbmgqrla&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=llvtlsjyoyiczbkjsxpf&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=xoebmbyexwuiogmbyprb&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=cwworuawihqvocglcoss&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=xshktygkujudfnjfioro&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=usrcshglbiilevmyfhse&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=xpbqleszmajjesnzddhv&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=bcoepfyewziejvcqyhqo&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=cslpybexmxyuacbyuvib&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=pwqnlynprfgtjbgqoizj&amp;fileformat=p2p&amp;archiveformat=gz"
        "http://list.iblocklist.com/?list=jhaoawihmfxgnvmaqffp&amp;fileformat=p2p&amp;archiveformat=gz")

[[ -f "big_list" ]] && rm big_list
touch big_list

echo "Downloading lists..."

for i in ${LISTS[@]}; do
    j=$(grep -E -o "=[a-z]{20}" <<< ${i})

    wget -O "${j#?}.gz" "${i}" --quiet --show-progress
    gunzip "${j#?}.gz"
    cat ${j#?} >> big_list

    rm ${j#?}
done

echo "All done!"
