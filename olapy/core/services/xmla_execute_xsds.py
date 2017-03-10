execute_xsd = """
<xs:schema elementFormDefault="qualified"
targetNamespace="urn:schemas-microsoft-com:xml-analysis:mddataset"
xmlns="urn:schemas-microsoft-com:xml-analysis:mddataset"
xmlns:xs="http://www.w3.org/2001/XMLSchema">
<xs:complexType name="MemberType">
    <xs:sequence>
        <xs:any maxOccurs="unbounded"
                    minOccurs="0"
                    namespace="##targetNamespace"
                    processContents="skip"/>
    </xs:sequence>
    <xs:attribute name="Hierarchy" type="xs:string"/>
</xs:complexType>
<xs:complexType name="PropType">
    <xs:sequence>
        <xs:element minOccurs="0" name="Default"/>
    </xs:sequence>
    <xs:attribute name="name" type="xs:string" use="required"/>
    <xs:attribute name="type" type="xs:QName"/>
</xs:complexType>
<xs:complexType name="TupleType">
    <xs:sequence>
        <xs:element maxOccurs="unbounded" name="Member" type="MemberType"/>
    </xs:sequence>
</xs:complexType>
<xs:complexType name="MembersType">
    <xs:sequence>
        <xs:element maxOccurs="unbounded" minOccurs="0" name="Member" type="MemberType"/>
    </xs:sequence>
    <xs:attribute name="Hierarchy" type="xs:string" use="required"/>
</xs:complexType>
<xs:complexType name="TuplesType">
    <xs:sequence>
        <xs:element maxOccurs="unbounded" minOccurs="0" name="Tuple" type="TupleType"/>
    </xs:sequence>
</xs:complexType>
<xs:group name="SetType">
    <xs:choice>
        <xs:element name="Members" type="MembersType"/>
        <xs:element name="Tuples" type="TuplesType"/>
        <xs:element name="CrossProduct" type="SetListType"/>
        <xs:element name="Union">
    <xs:complexType>
        <xs:group maxOccurs="unbounded" minOccurs="0" ref="SetType"/>
    </xs:complexType>
    </xs:element>
    </xs:choice>
</xs:group>
<xs:complexType name="SetListType">
    <xs:group maxOccurs="unbounded" minOccurs="0" ref="SetType"/>
    <xs:attribute name="Size" type="xs:unsignedInt"/>
</xs:complexType>
<xs:complexType name="OlapInfo">
    <xs:sequence>
    <xs:element name="CubeInfo">
<xs:complexType>
<xs:sequence>
    <xs:element maxOccurs="unbounded" name="Cube">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="CubeName" type="xs:string"/>
            <xs:element minOccurs="0" name="LastDataUpdate" type="xs:dateTime"/>
            <xs:element minOccurs="0" name="LastSchemaUpdate" type="xs:dateTime"/>
        </xs:sequence>
        </xs:complexType>
        </xs:element>
        </xs:sequence>
    </xs:complexType>
    </xs:element>
    <xs:element name="AxesInfo">
        <xs:complexType>
            <xs:sequence>
            <xs:element maxOccurs="unbounded" name="AxisInfo">
            <xs:complexType>
                <xs:sequence>
                    <xs:element maxOccurs="unbounded" minOccurs="0" name="HierarchyInfo">
                        <xs:complexType>
                            <xs:sequence>
                                <xs:any maxOccurs="unbounded" minOccurs="0" namespace="##targetNamespace"
                                processContents="skip"/>
                            </xs:sequence>
                            <xs:attribute name="name" type="xs:string" use="required"/>
                        </xs:complexType>
                    </xs:element>
                </xs:sequence>
                <xs:attribute name="name" type="xs:string"/>
            </xs:complexType>
            </xs:element>
            </xs:sequence>
        </xs:complexType>
        </xs:element>
        <xs:element name="CellInfo">
        <xs:complexType>
            <xs:choice maxOccurs="unbounded" minOccurs="0">
            <xs:any maxOccurs="unbounded" minOccurs="0" namespace="##targetNamespace" processContents="skip"/>
            </xs:choice>
        </xs:complexType>
        </xs:element>
        </xs:sequence>
    </xs:complexType>
    <xs:complexType name="Axes">
        <xs:sequence>
            <xs:element maxOccurs="unbounded" name="Axis">
            <xs:complexType>
                <xs:group maxOccurs="unbounded" minOccurs="0" ref="SetType"/>
                <xs:attribute name="name" type="xs:string"/>
            </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>
    <xs:complexType name="CellData">
        <xs:sequence>
            <xs:element maxOccurs="unbounded" minOccurs="0" name="Cell">
                <xs:complexType>
                    <xs:sequence>
                        <xs:any maxOccurs="unbounded" minOccurs="0" namespace="##targetNamespace"
                        processContents="skip"/>
                    </xs:sequence>
                    <xs:attribute name="CellOrdinal" type="xs:unsignedInt" use="required"/>
                </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>
    <xs:element name="root">
        <xs:complexType>
            <xs:sequence>
                <xs:any minOccurs="0" namespace="http://www.w3.org/2001/XMLSchema" processContents="strict"/>
                <xs:element minOccurs="0" name="OlapInfo" type="OlapInfo"/>
                <xs:element minOccurs="0" name="Axes" type="Axes"/>
                <xs:element minOccurs="0" name="CellData" type="CellData"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>"""