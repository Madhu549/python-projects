#!/bin/bash
set -x
SCRIPT=ckpkg
EMAIL=jakira.shaik@vodafone.com,madhubabu.tammu@vodafone.com
logfolderpkg=/opt/SP/scripts/ckpkage; loglpkg=$logfolderpkg/logs; dnloglpkg=$loglpkg/dnlogl; logcpkg=$logfolderpkg/config; sfilepkg=$logcpkg/sourceinfo;
tfilepkg=$logcpkg/targetinfo; orghostnamepkg=$logcpkg/org_hostname; lgdetpkg=$loglpkg/mail.log; bodypkg='Below hostname not rechable, Please check and take immediate action'
echo $logfolderpkg $loglpkg $dnloglpkg $logcpkg $sfilepkg $tfilepkg $orghostnamepkg $lgdetpkg $bodypkg
SCRIPTLGpkg=$loglpkg/$SCRIPT.log; cat /dev/null > $dnloglpkg; cat /dev/null > $SCRIPTLGpkg
echo " The $SCRIPT script has started on `date`"  >> $SCRIPTLGpkg
countsfile=`cat $sfilepkg | wc -l`; counttfile=`cat $tfilepkg | wc -l`;  countsfilew=`awk -F"-" '{print NF}' $sfilepkg`; counttfilew=`awk -F"-" '{print NF}' $tfilepkg`

if [[ "$countsfile" -eq 1  && $counttfile -eq 1  && "$countsfilew" -eq 3  &&  $counttfilew -eq 3 ]] ; then echo " $sfilepkg $tfilepkg input files are ok to proceed" >> $SCRIPTLGpkg; else echo "existing from code package-version-check Please check input file $sfilepkg $tfilepkg and $orghostnamepkg" >> $SCRIPTLGpkg;  echo "existing from code package-version-check Please check input file $sfilepkg $tfilepkg and $orghostnamepkg" | mail -s "existing from code package-version-check Please check input file" "$EMAIL"; exit; fi
szone=`cat $sfilepkg | awk -F "-" '{print $1}'`; sgrepenv=`cat $sfilepkg | awk -F "-" '{print $2}'`; sgrepdc=`cat $sfilepkg | awk -F "-" '{print $3}'`; echo $szone $sgrepenv $sgrepdc >> $SCRIPTLGpkg
tzone=`cat $tfilepkg | awk -F "-" '{print $1}'`; tgrepenv=`cat $tfilepkg | awk -F "-" '{print $2}'`; tgrepdc=`cat $tfilepkg | awk -F "-" '{print $3}'`; echo $tzone $tgrepenv $tgrepdc >> $SCRIPTLGpkg
dd=$(date +"%d%m%Y_%H%M%S"); pp1=`cat $orghostnamepkg | grep -w $sgrepenv | grep -w $sgrepdc | grep -w $szone`; pp1c=`echo $pp1 | wc -l`; echo $pp1 $pp1c >> $SCRIPTLGpkg
sszone=`echo $pp1 | awk -F "$" '{print $1}'`; ssgrepenv=`echo $pp1 | awk -F "$" '{print $4}'`; ssgrepdc=`echo $pp1 | awk -F "$" '{print $5}'`
sspath=`echo $pp1 | awk -F "$" '{print $3}'`; gsspath=`echo $sspath | awk -F "/{" '{print $1}'`; shust=`echo $pp1 | awk -F "$" '{print $2}'`; sipadd=`echo $shust | awk -F "@" '{print $2}'`; 
echo $sszone $ssgrepenv $ssgrepdc $shust $sipadd $sspath  $gsspath>> $SCRIPTLGpkg
pp2=`cat $orghostnamepkg | grep -w $tgrepenv | grep -w $tgrepdc | grep -w $tzone`; pp2c=`echo $pp2 | wc -l`; echo $pp2 $pp2c >> $SCRIPTLGpkg
ttzone=`echo $pp2 | awk -F "$" '{print $1}'`; ttgrepenv=`echo $pp2 | awk -F "$" '{print $4}'`; ttgrepdc=`echo $pp2 | awk -F "$" '{print $5}'`
ttpath=`echo $pp2 | awk -F "$" '{print $3}'`; gttpath=`echo $ttpath | awk -F "/{" '{print $1}'`; thust=`echo $pp2 | awk -F "$" '{print $2}'`; tipadd=`echo $thust | awk -F "@" '{print $2}'`; echo $ttzone $ttgrepenv $ttgrepdc $thust $tipadd $ttpath $gttpath >> $SCRIPTLGpkg

cat /dev/null > $SCRIPTLGpkg
rm  "${loglpkg}"/*srcpkgpatn  "${loglpkg}"/*tgtpkgpatn "${loglpkg}"/results_srcpkgpatn "${loglpkg}"/*csv
        if [[ "$szone" = "$sszone"  && "$sgrepenv" = "$ssgrepenv"  && "$sgrepdc" = "$ssgrepdc" && "$tzone" = "$ttzone" && "$tgrepenv" = "$ttgrepenv" && "$tgrepdc" = "$ttgrepdc" ]] ; then
                ssh -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no -o LogLevel=quiet  "$shust" exit
                s_rslt=$?
                ssh -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no -o LogLevel=quiet  "$thust" exit
                t_rslt=$?
                if [[ "$s_rslt" -eq 0 ]] && [[ $t_rslt -eq 0 ]]; then echo -e "connected to $hust host `date`" >> $SCRIPTLGpkg
					ssh -n -q "$shust" "find $sspath -type f -name manifest.v3 -exec grep -A3 -e '<value name=\"enabled\">' {} +" >  "${loglpkg}"/1_srcpkgpatn
					ssh -n -q "$thust" "find $ttpath -type f -name manifest.v3 -exec grep -A3 -e '<value name=\"enabled\">' {} +" > "${loglpkg}"/1_tgtpkgpatn
					#for ((i=1; i<=20; i++)); do echo "wm$i"; done 
					
					cat "${loglpkg}"/1_srcpkgpatn | grep -e '<value name="enabled">' | fgrep $gsspath/wm > $loglpkg/senabledstatus_srcpkgpatn
					cat "${loglpkg}"/1_srcpkgpatn | grep -e '<value name="version">' | fgrep $gsspath/wm > $loglpkg/sversionstatus_srcpkgpatn
					cat "${loglpkg}"/senabledstatus_srcpkgpatn | awk -F ':' '{print $1}' > $loglpkg/spkgliststatus_srcpkgpatn
					
					cat "${loglpkg}"/1_tgtpkgpatn | grep -e '<value name="enabled">' | fgrep $gttpath/wm > $loglpkg/tenabledstatus_tgtpkgpatn
					cat "${loglpkg}"/1_tgtpkgpatn | grep -e '<value name="version">' | fgrep $gttpath/wm > $loglpkg/tversionstatus_tgtpkgpatn

                    while read pkgname; do
                        spkgsenabled=`fgrep $pkgname $loglpkg/senabledstatus_srcpkgpatn | grep -i enabled | awk -F '<value name="enabled">'  '{print $2}' | awk -F '</value>' '{print $1}'`
                        spkgsenabledc=`fgrep $pkgname $loglpkg/senabledstatus_srcpkgpatn | grep -i enabled | awk -F '<value name="enabled">'  '{print $2}' | awk -F '</value>' '{print $1}' | wc -l`
                        spkgsver=`fgrep $pkgname $loglpkg/sversionstatus_srcpkgpatn | grep -e '<value name="version">' | awk -F '<value name="version">'  '{print $2}' | awk -F '</value>' '{print $1}'`
                        spkgsverc=`fgrep $pkgname $loglpkg/sversionstatus_srcpkgpatn | grep -e '<value name="version">' | awk -F '<value name="version">'  '{print $2}' | awk -F '</value>' '{print $1}' | wc -l`
						sgrepinstance=`fgrep $pkgname $loglpkg/senabledstatus_srcpkgpatn | grep -i enabled | awk -F "$gsspath" '{print $2}' | awk -F "/packages/" '{print $1}' | sed -e 's/\///g'`
						
                        tpkgsenabled=`fgrep $pkgname $loglpkg/tenabledstatus_tgtpkgpatn | grep -i enabled | awk -F '<value name="enabled">'  '{print $2}' | awk -F '</value>' '{print $1}'`
                        tpkgsver=`fgrep $pkgname $loglpkg/tversionstatus_tgtpkgpatn | grep -e '<value name="version">' | awk -F '<value name="version">'  '{print $2}' | awk -F '</value>' '{print $1}'`
                        tpkgsenabledc=`fgrep $pkgname $loglpkg/tenabledstatus_tgtpkgpatn | grep -i enabled | awk -F '<value name="enabled">'  '{print $2}' | awk -F '</value>' '{print $1}' | wc -l`
                        tpkgsverc=`fgrep $pkgname $loglpkg/tversionstatus_tgtpkgpatn | grep -e '<value name="version">' | awk -F '<value name="version">'  '{print $2}' | awk -F '</value>' '{print $1}' | wc -l`
						tgrepinstance=`fgrep $pkgname $loglpkg/tenabledstatus_tgtpkgpatn | grep -i enabled | awk -F "$gttpath" '{print $2}' | awk -F "/packages/" '{print $1}' | sed -e 's/\///g'`
						
                        sorgpkgnme=`echo $pkgname | awk -F 'packages' '{print $2}' |  awk -F 'manifest.v3' '{print $1}' | sed -e 's/\///g'`
                        torgpkgnme=`fgrep $pkgname $loglpkg/tenabledstatus_tgtpkgpatn | grep -i enabled | awk -F 'packages' '{print $2}'  |  awk -F 'manifest.v3' '{print $1}' | sed -e 's/\///g'`
                        sorgpkgnmec=`echo $pkgname | awk -F 'packages' '{print $2}' |  awk -F 'manifest.v3' '{print $1}' | sed -e 's/\///g' | wc -l`
                        torgpkgnmec=`fgrep $pkgname $loglpkg/tenabledstatus_tgtpkgpatn | grep -i enabled | awk -F 'packages' '{print $2}'  |  awk -F 'manifest.v3' '{print $1}' | sed -e 's/\///g' | wc -l`

                        #if [[ "$spkgsenabledc" -eq 1  && $spkgsverc -eq 1  && "$tpkgsenabledc" -eq 1  &&  $tpkgsverc -eq 1 && "$sorgpkgnmec" -eq 1  &&  $torgpkgnmec -eq 1 ]] ; then
                                echo "ok to proceed with all 1 counts $spkgsenabledc $spkgsverc $tpkgsenabledc $tpkgsverc $sorgpkgnmec $torgpkgnmec both are same" >> $SCRIPTLGpkg
                                if [ -n "$sorgpkgnme" ]; then sorgpkgnme="${sorgpkgnme}"; else sorgpkgnme=null; fi
								if [ -n "$torgpkgnme" ]; then torgpkgnme="${torgpkgnme}"; else torgpkgnme=nu11; fi
								if [ -n "$spkgsenabled" ]; then spkgsenabled="${spkgsenabled}"; else spkgsenabled=nu11; fi
								if [ -n "$tpkgsenabled" ]; then tpkgsenabled="${tpkgsenabled}"; else tpkgsenabled=nu11; fi
								#if [ -n "$spkgsver" ]; then spkgsver="${spkgsver}"; else spkgsver=nu11; fi
								#if [ -n "$tpkgsver" ]; then tpkgsver="${tpkgsver}"; else tpkgsver=nu11; fi
								if [ -n "$sgrepinstance" ]; then sgrepinstance="${sgrepinstance}"; else sgrepinstance=nu11; fi
								if [ -n "$tgrepinstance" ]; then tgrepinstance="${tgrepinstance}"; else tgrepinstance=nu11; fi
								if [ -n "$spkgsver" ]; then sspkgsver="${spkgsver}"; else sspkgsver=nu11; fi
								if [ -n "$tpkgsver" ]; then ttpkgsver="${tpkgsver}"; else ttpkgsver=nu11; fi
								
                                if [ "$sorgpkgnme" = "$torgpkgnme" ]; then
                                        echo "$sorgpkgnme $torgpkgnme both are same package-names" >> $SCRIPTLGpkg
										if [[ "$spkgsenabled" = yes  && "$tpkgsenabled" = yes ]]; then
													source_pkg_status_check=Enabled
													target_pkg_status_check=Enabled
											elif [[ "$spkgsenabled" = yes  && "$tpkgsenabled" = no ]]; then
													source_pkg_status_check=Enabled
													target_pkg_status_check=Disabled
											elif [[ "$spkgsenabled" = no  && "$tpkgsenabled" = yes ]]; then
													source_pkg_status_check=Disabled
													target_pkg_status_check=Enabled
											elif [[ "$spkgsenabled" = no  && "$tpkgsenabled" = no ]]; then
													source_pkg_status_check=Disabled
													target_pkg_status_check=Disabled
											elif [[ "$spkgsenabled" = yes  && "$tpkgsenabled" = null ]]; then
													source_pkg_status_check=Disabled
													target_pkg_status_check=null
											elif [[ "$spkgsenabled" = null  && "$tpkgsenabled" = yes ]]; then
													source_pkg_status_check=null
													target_pkg_status_check=Enabled
											elif [[ "$spkgsenabled" = null  && "$tpkgsenabled" = null ]]; then
													source_pkg_status_check=null
													target_pkg_status_check=null
											elif [[ "$spkgsenabled" = no  && "$tpkgsenabled" = null ]]; then
													source_pkg_status_check=Disabled
													target_pkg_status_check=null
											elif [[ "$spkgsenabled" = null  && "$tpkgsenabled" = no ]]; then
													source_pkg_status_check=null
													target_pkg_status_check=Disabled

											else 
													source_pkg_status_check=Unknown-Error
													target_pkg_status_check=Unknown-Error
										fi


											if [ "$sspkgsver" = "$ttpkgsver" ]; then
													echo "$szone" "$sgrepdc" "$tgrepdc" "$sipadd" "$tipadd" "$sgrepenv" "$tgrepenv" "$sgrepinstance" "$sorgpkgnme" "$source_pkg_status_check" "$target_pkg_status_check" "$sspkgsver" pkg-ver-Matched >> $loglpkg/results_srcpkgpatn
													echo "$szone" "$sgrepdc" "$tgrepdc" "$sipadd" "$tipadd" "$sgrepenv" "$tgrepenv" "$sgrepinstance" "$sorgpkgnme" "$source_pkg_status_check" "$target_pkg_status_check" "$sspkgsver" pkg-ver-Matched >> $SCRIPTLGpkg
													else
													echo "$szone" "$sgrepdc" "$tgrepdc" "$sipadd" "$tipadd" "$sgrepenv" "$tgrepenv" "$sgrepinstance" "$sorgpkgnme" "$source_pkg_status_check" "$target_pkg_status_check" "$sspkgsver" pkg-ver-mismatch-$ttpkgsver >> $loglpkg/results_srcpkgpatn
													echo "$szone" "$sgrepdc" "$tgrepdc" "$sipadd" "$tipadd" "$sgrepenv" "$tgrepenv" "$sgrepinstance" "$sorgpkgnme" "$source_pkg_status_check" "$target_pkg_status_check" "$sspkgsver" pkg-ver-mismatch-$ttpkgsver >> $SCRIPTLGpkg
													
											fi										
										
                                    else 
										
										
										target_pkg_status_check=PKG-doent-exit
										echo $sorgpkgnme | grep -i yes
										if [[ $? == 0 ]] ; then source_pkg_status_check=Enabled; else  source_pkg_status_check=Disabled; fi
										#target_pkg_status_check=NA
										sspkgsver=NA
										ttpkgsver=NA
										echo "$szone" "$sgrepdc" "$tgrepdc" "$sipadd" "$tipadd" "$sgrepenv" "$tgrepenv" "$sgrepinstance" "$sorgpkgnme" "$source_pkg_status_check" "$target_pkg_status_check" "$sspkgsver" pkg-ver-mismatch-$ttpkgsver >> $loglpkg/results_srcpkgpatn
                                        echo "$szone" "$sgrepdc" "$tgrepdc" "$sipadd" "$tipadd" "$sgrepenv" "$tgrepenv" "$sgrepinstance" "$sorgpkgnme" "$source_pkg_status_check" "$target_pkg_status_check" "$sspkgsver" pkg-ver-mismatch-$ttpkgsver  >> $SCRIPTLGpkg
                                fi
                                	echo "source pkg is $source_pkg_status_check and target is $target_pkg_status_check" >> $SCRIPTLGpkg
                                #else echo "$szone" "$sgrepdc" "$sipadd" "$sgrepenv" "$sgrepinstance" "$sorgpkgnme" Enabled Unknown-Error Unknown-Error Unknown-Error >> $loglpkg/results_srcpkgpatn
								#echo "NOT-ok to proceed with all 1 counts sss $pkgname $spkgsenabledc $spkgsverc $tpkgsenabledc $tpkgsverc $sorgpkgnmec $torgpkgnmec both are not-same" >> $SCRIPTLGpkg
								#fi
                                unset pkgname spkgsenabled spkgsver sspkgsver tpkgsenabled tpkgsver ttpkgsver sorgpkgnme torgpkgnme source_pkg_status_check target_pkg_status_check spkgsenabledc spkgsverc tpkgsenabledc tpkgsverc sorgpkgnmec torgpkgnmec sgrepinstance tgrepinstance


                    done < $loglpkg/spkgliststatus_srcpkgpatn
							mcount=`cat $loglpkg/results_srcpkgpatn | wc -l`
							if [ $mcount -gt 1 ]; then
								sed -i -e '1isource-zone source-DC Target-DC source-IP Target-IP source-ENV Target-ENV Instance Source-Package-name source-package-status target-package-status source-version target-version\' $loglpkg/results_srcpkgpatn
								sed 's/ \+/,/g' "${loglpkg}"/results_srcpkgpatn > "${loglpkg}"/"$dd"_${sgrepenv}_"$szone"_${sgrepdc}.csv
								echo `date` "${loglpkg}"/"$dd"_${sgrepenv}_"$szone"_${sgrepdc}.csv | mail -s "Package status report from $sgrepdc $szone $sgrepenv " -a "${loglpkg}"/"$dd"_${sgrepenv}_"$szone"_${sgrepdc}.csv "$EMAIL"
								echo -e " successfully generated .csv file "${loglpkg}"/"$dd"_${sgrepenv}_"$szone"_${sgrepdc}.csv and mailed to $EMAIL at `date` for $sgrepdc $szone $sgrepenv  " >> $SCRIPTLGpkg
								else
								echo no-match-file >> $SCRIPTLGpkg
							fi

                        else echo -e "Either one of the hostname $shust or $thust is down or not rechable terminating the program `date`" | tee -a $SCRIPTLG >> $dnlogl; exit
                fi
                else
                        echo -e "Please provide valid inputs parameters in file $sfilepkg $tfilepkg and check configuration file $orghostnamepkg or refer documentation manual `date`" | mail -s "Invalid inputs parameters provided for package verification script`date`" "$EMAIL"
                        echo -e "terminating the program, Please provide valid inputs parameters in file $sfilepkg $tfilepkg and check configuration file $orghostnamepkg or refer documentation manual `date`" >> $SCRIPTLGpkg; exit

        fi
echo " The $SCRIPT script has ended on `date`"  >> $SCRIPTLGpkg
unset SCRIPT EMAIL logfolderpkg loglpkg dnloglpkg logcpkg sfilepkg tfilepkg orghostnamepkg lgdetpkg bodypkg SCRIPTLGpkg countsfile counttfile countsfilew counttfilew szone sgrepenv sgrepdc tzone tgrepenv tgrepdc pp1 pp1c sszone ssgrepenv ssgrepdc shust sipadd sspath  gsspath pp2 pp2c ttzone ttgrepenv ttgrepdc thust tipadd ttpath gttpath s_rslt t_rslt mcount
